from PySide2 import QtWidgets, QtCore, QtGui, QtMultimedia
from glob import glob

import os, json
import eyed3


class MainWindow(QtWidgets.QWidget):

    def __init__(self, appctxt):
        super().__init__()
        self.setFixedSize(650, 350)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.rectangle = self.frameGeometry()
        self.centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        self.rectangle.moveCenter(self.centerPoint)
        self.move(self.rectangle.topLeft())
        self.appctxt = appctxt
        self.cur_dir = os.path.expanduser("~")
        self.setup_ui()

    def setup_ui(self):
        self.create_widgets()
        self.create_sys_tray_icon()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.setup_connections()
        self.settings_menu()
        self.open_settings()
        self.quicksetup()
        self.get_musics()

    #  Ui--------------------------------------------------------

    def create_widgets(self):
        self.btn_close = QtWidgets.QPushButton()
        self.btn_max = QtWidgets.QPushButton()
        self.btn_min = QtWidgets.QPushButton()

        self.btn_play = QtWidgets.QPushButton()
        self.btn_next = QtWidgets.QPushButton()
        self.btn_back = QtWidgets.QPushButton()
        self.btn_stop = QtWidgets.QPushButton()

        self.btn_easter_egg = QtWidgets.QPushButton()

        self.lb_title = QtWidgets.QLabel("A+Music Player")
        self.lb_time = QtWidgets.QLabel("0:0 / 0:0")
        self.lb_volume = QtWidgets.QLabel()
        self.lb_img_volume = QtWidgets.QLabel()

        self.time_bar = QtWidgets.QSlider()

        self.list = QtWidgets.QListWidget()

        self.setts = QtWidgets.QMenu()
        self.btn_setts = QtWidgets.QPushButton()

        self.sl_volume = QtWidgets.QSlider()

    def create_sys_tray_icon(self):
        self.tray = QtWidgets.QSystemTrayIcon()
        self.tray.setIcon(QtGui.QIcon(self.appctxt.get_resource("icon.png")))
        self.tray.setVisible(True)
        self.tray_menu = QtWidgets.QMenu()
        self.tray_menu.addAction(QtGui.QIcon(self.appctxt.get_resource("play.png")), "Play/Pause", self.play_pause)
        self.tray_menu.addAction(QtGui.QIcon(self.appctxt.get_resource("next.png")), "Next", self.next)
        self.tray_menu.addAction(QtGui.QIcon(self.appctxt.get_resource("back.png")), "Previous", self.back)
        self.tray_menu.addAction(QtGui.QIcon(self.appctxt.get_resource("stop.png")), "Stop", self.stop)
        self.tray_menu.addAction(QtGui.QIcon(self.appctxt.get_resource("close.png")), "Show/Hide", self.showhide)
        self.tray.setContextMenu(self.tray_menu)

    def modify_widgets(self):
        self.btn_easter_egg.setFixedSize(25, 35)

        self.set_btn_size([self.btn_close,
                           self.btn_max,
                           self.btn_min,
                           self.btn_play,
                           self.btn_next,
                           self.btn_back,
                           self.btn_stop], 25, 25)

        self.set_btn_flat([self.btn_close,
                           self.btn_max,
                           self.btn_min,
                           self.btn_play,
                           self.btn_next,
                           self.btn_back,
                           self.btn_stop,
                           self.btn_setts,
                           self.btn_easter_egg], True)

        self.set_btn_icon([self.btn_close,
                           self.btn_max,
                           self.btn_min,
                           self.btn_play,
                           self.btn_next,
                           self.btn_back,
                           self.btn_stop,
                           self.btn_setts],
                          [self.appctxt.get_resource("close.png"),
                           self.appctxt.get_resource("maximize.png"),
                           self.appctxt.get_resource("min.png"),
                           self.appctxt.get_resource("play.png"),
                           self.appctxt.get_resource("next.png"),
                           self.appctxt.get_resource("back.png"),
                           self.appctxt.get_resource("stop.png"),
                           self.appctxt.get_resource("more.png")])

        self.lb_title.setFont(QtGui.QFont("Bahnschrift SemiBold SemiConden", 25))
        self.lb_title.setAlignment(QtCore.Qt.AlignTop)
        self.lb_title.setStyleSheet("QLabel { color : red; }")
        self.lb_time.setFont(QtGui.QFont("Bahnschrift SemiBold SemiConden", 12))
        self.lb_time.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_volume.setFont(QtGui.QFont("Bahnschrift SemiBold SemiConden", 12))
        self.lb_volume.setAlignment(QtCore.Qt.AlignCenter)

        self.time_bar.setOrientation(QtCore.Qt.Horizontal)

        self.list.setDragEnabled(False)

        self.btn_setts.setMenu(self.setts)
        self.btn_setts.setFixedSize(45, 25)

        self.time_bar.setStyleSheet("""QSlider::groove:horizontal {
    border: 1px;
    height: 10px;
    background: lightgray;
}

QSlider::handle:horizontal {
    background: red;
    border: 1px;
    width: 5px;
    margin: -5px 0;
    border-radius: 2px;
}

QSlider::sub-page:horizontal {
    background: lightblue;
}""")
        self.sl_volume.installEventFilter(self)
        self.sl_volume.setMouseTracking(True)
        self.sl_volume.setPageStep(1)

        self.sl_volume.setOrientation(QtCore.Qt.Horizontal)
        self.sl_volume.setStyleSheet("""QSlider::groove:horizontal {
    border: 1px;
    height: 10px;
    background: lightgray;
}

QSlider::handle:horizontal {
    background: red;
    border: 1px;
    width: 5px;
    margin: -5px 0;
    border-radius: 2px;
}

QSlider::sub-page:horizontal {
    background: lightblue;
}""")
        self.sl_volume.setRange(0, 100)

        self.pix = QtGui.QPixmap(self.appctxt.get_resource("volume.png"))

        self.lb_img_volume.setPixmap(self.pix.scaled(25, 25))
        self.lb_img_volume.setFixedSize(25, 25)
        self.lb_img_volume.setMouseTracking(True)
        self.lb_img_volume.installEventFilter(self)
        self.lb_img_volume.setAlignment(QtCore.Qt.AlignCenter)

        self.lb_volume.installEventFilter(self)
        self.lb_volume.setMouseTracking(True)

        self.lb_volume.setHidden(True)
        self.sl_volume.setHidden(True)

    def create_layouts(self):
        self.main_layout = QtWidgets.QGridLayout(self)

    def add_widgets_to_layouts(self):
        self.main_layout.addWidget(self.btn_close, 1, 21, 1, 1)
        self.main_layout.addWidget(self.btn_max, 1, 20, 1, 1)
        self.main_layout.addWidget(self.btn_min, 1, 19, 1, 1)
        self.main_layout.addWidget(self.lb_title, 1, 1, 2, 11)
        self.main_layout.addWidget(self.lb_time, 5, 19, 1, 3)
        self.main_layout.addWidget(self.btn_play, 5, 2, 1, 1)
        self.main_layout.addWidget(self.btn_back, 5, 1, 1, 1)
        self.main_layout.addWidget(self.btn_next, 5, 3, 1, 1)
        self.main_layout.addWidget(self.btn_stop, 5, 4, 1, 1)
        self.main_layout.addWidget(self.list, 3, 1, 1, 21)
        self.main_layout.addWidget(self.btn_setts, 1, 18, 1, 1)
        self.main_layout.addWidget(self.lb_img_volume, 5, 18, 1, 1)
        self.main_layout.addWidget(self.time_bar, 5, 5, 1, 13)
        self.main_layout.addWidget(self.btn_easter_egg, 1, 1, 2, 1)

    def setup_connections(self):
        self.btn_close.clicked.connect(self.close)
        self.btn_max.clicked.connect(self.max)
        self.btn_min.clicked.connect(self.showMinimized)
        self.list.itemClicked.connect(self.read_file)
        self.list.itemDoubleClicked.connect(self.modify_details)
        self.btn_play.clicked.connect(self.play_pause)
        self.btn_stop.clicked.connect(self.stop)
        self.time_bar.sliderReleased.connect(self.set_time)
        self.btn_next.clicked.connect(self.next)
        self.btn_back.clicked.connect(self.back)
        self.btn_easter_egg.clicked.connect(self.easter_egg)
        self.sl_volume.valueChanged.connect(self.set_volume)

    #  Methods---------------------------------------------------

    def about(self):
        self.win = QtWidgets.QMessageBox()
        self.win.setWindowTitle("A+Music | About")
        self.win.setText("""A+Music is a basic music player wich is now playing only mp3.
This app is open-sourced. Therefore, you can edit the code as you wish.
This app has been developped by a teenager who is learning.
If you read this, you're God!
(Also, click once on the "A" of A+Music...)
(You can click another time on it to disable the thing.)


ΔINDUSTRIES© 2020.""")
        self.win.exec_()

    def back(self):
        self.nbr = self.list.currentRow() - 1
        if not self.nbr == -1:
            self.list.setCurrentRow(self.list.currentRow() - 1)
        else:
            self.list.setCurrentRow(self.list.count() - 1)
            self.nbr = self.list.count() - 1
        self.read_file()

    def closeEvent(self, event: QtGui.QCloseEvent):
        self.save_settings()

    def easter_egg(self):
        if self.settings["easter_egg_on"] == False:
            self.easter_egg_timer = QtCore.QTimer()
            self.easter_egg_timer.setInterval(100)
            self.easter_egg_timer.timeout.connect(self.easter_egg_animate)
            self.easter_egg_color_nbr = 0
            self.easter_egg_timer.start()
            self.settings["easter_egg_on"] = True
            self.save_settings()
        elif self.settings["easter_egg_on"] == True:
            self.easter_egg_timer.stop()
            self.lb_title.setStyleSheet("QLabel { color : red; }")
            self.list.setStyleSheet("QListWidget::item { color : black; }")
            self.sl_volume.setStyleSheet("""QSlider::groove:horizontal {
                            border: 1px;
                            height: 10px;
                            background: lightgray;
                        }

                        QSlider::handle:horizontal {
                            background: red;
                            border: 1px;
                            width: 5px;
                            margin: -5px 0;
                            border-radius: 2px;
                        }

                        QSlider::sub-page:horizontal {
                            background: lightblue;
                        }""")
            self.time_bar.setStyleSheet("""QSlider::groove:horizontal {
                            border: 1px;
                            height: 10px;
                            background: lightgray;
                        }

                        QSlider::handle:horizontal {
                            background: red;
                            border: 1px;
                            width: 5px;
                            margin: -5px 0;
                            border-radius: 2px;
                        }

                        QSlider::sub-page:horizontal {
                            background: lightblue;
                        }""")
            self.settings["easter_egg_on"] = False
            self.save_settings()

    def easter_egg_animate(self):
        if self.easter_egg_color_nbr == 0:
            self.lb_title.setStyleSheet("QLabel { color : red; }")
            self.list.setStyleSheet("QListWidget::item { color : red; }")
            self.time_bar.setStyleSheet("""QSlider::groove:horizontal {
                border: 1px;
                height: 10px;
                background: lightgray;
            }

            QSlider::handle:horizontal {
                background: red;
                border: 1px;
                width: 5px;
                margin: -5px 0;
                border-radius: 2px;
            }

            QSlider::sub-page:horizontal {
                background: red;
            }""")
            self.sl_volume.setStyleSheet("""QSlider::groove:horizontal {
                border: 1px;
                height: 10px;
                background: lightgray;
            }

            QSlider::handle:horizontal {
                background: red;
                border: 1px;
                width: 5px;
                margin: -5px 0;
                border-radius: 2px;
            }

            QSlider::sub-page:horizontal {
                background: red;
            }""")
            self.easter_egg_color_nbr += 1
        elif self.easter_egg_color_nbr == 1:
            self.lb_title.setStyleSheet("QLabel { color : orange; }")
            self.list.setStyleSheet("QListWidget::item { color : orange; }")
            self.time_bar.setStyleSheet("""QSlider::groove:horizontal {
                border: 1px;
                height: 10px;
                background: lightgray;
            }

            QSlider::handle:horizontal {
                background: red;
                border: 1px;
                width: 5px;
                margin: -5px 0;
                border-radius: 2px;
            }

            QSlider::sub-page:horizontal {
                background: orange;
            }""")
            self.sl_volume.setStyleSheet("""QSlider::groove:horizontal {
                border: 1px;
                height: 10px;
                background: lightgray;
            }

            QSlider::handle:horizontal {
                background: red;
                border: 1px;
                width: 5px;
                margin: -5px 0;
                border-radius: 2px;
            }

            QSlider::sub-page:horizontal {
                background: orange;
            }""")
            self.easter_egg_color_nbr += 1
        elif self.easter_egg_color_nbr == 2:
            self.lb_title.setStyleSheet("QLabel { color : yellow; }")
            self.list.setStyleSheet("QListWidget::item { color : yellow; }")
            self.time_bar.setStyleSheet("""QSlider::groove:horizontal {
                border: 1px;
                height: 10px;
                background: lightgray;
            }

            QSlider::handle:horizontal {
                background: red;
                border: 1px;
                width: 5px;
                margin: -5px 0;
                border-radius: 2px;
            }

            QSlider::sub-page:horizontal {
                background: yellow;
            }""")
            self.sl_volume.setStyleSheet("""QSlider::groove:horizontal {
                border: 1px;
                height: 10px;
                background: lightgray;
            }

            QSlider::handle:horizontal {
                background: red;
                border: 1px;
                width: 5px;
                margin: -5px 0;
                border-radius: 2px;
            }

            QSlider::sub-page:horizontal {
                background: yellow;
            }""")
            self.easter_egg_color_nbr += 1
        elif self.easter_egg_color_nbr == 3:
            self.lb_title.setStyleSheet("QLabel { color : green; }")
            self.list.setStyleSheet("QListWidget::item { color : green; }")
            self.time_bar.setStyleSheet("""QSlider::groove:horizontal {
                border: 1px;
                height: 10px;
                background: lightgray;
            }

            QSlider::handle:horizontal {
                background: red;
                border: 1px;
                width: 5px;
                margin: -5px 0;
                border-radius: 2px;
            }

            QSlider::sub-page:horizontal {
                background: green;
            }""")
            self.sl_volume.setStyleSheet("""QSlider::groove:horizontal {
                border: 1px;
                height: 10px;
                background: lightgray;
            }

            QSlider::handle:horizontal {
                background: red;
                border: 1px;
                width: 5px;
                margin: -5px 0;
                border-radius: 2px;
            }

            QSlider::sub-page:horizontal {
                background: green;
            }""")
            self.easter_egg_color_nbr += 1
        elif self.easter_egg_color_nbr == 4:
            self.lb_title.setStyleSheet("QLabel { color : blue; }")
            self.list.setStyleSheet("QListWidget::item { color : blue; }")
            self.time_bar.setStyleSheet("""QSlider::groove:horizontal {
                border: 1px;
                height: 10px;
                background: lightgray;
            }

            QSlider::handle:horizontal {
                background: red;
                border: 1px;
                width: 5px;
                margin: -5px 0;
                border-radius: 2px;
            }

            QSlider::sub-page:horizontal {
                background: blue;
            }""")
            self.sl_volume.setStyleSheet("""QSlider::groove:horizontal {
                border: 1px;
                height: 10px;
                background: lightgray;
            }

            QSlider::handle:horizontal {
                background: red;
                border: 1px;
                width: 5px;
                margin: -5px 0;
                border-radius: 2px;
            }

            QSlider::sub-page:horizontal {
                background: blue;
            }""")
            self.easter_egg_color_nbr += 1
        elif self.easter_egg_color_nbr == 5:
            self.lb_title.setStyleSheet("QLabel { color : purple; }")
            self.list.setStyleSheet("QListWidget::item { color : purple; }")
            self.time_bar.setStyleSheet("""QSlider::groove:horizontal {
                border: 1px;
                height: 10px;
                background: lightgray;
            }

            QSlider::handle:horizontal {
                background: red;
                border: 1px;
                width: 5px;
                margin: -5px 0;
                border-radius: 2px;
            }

            QSlider::sub-page:horizontal {
                background: purple;
            }""")
            self.sl_volume.setStyleSheet("""QSlider::groove:horizontal {
                border: 1px;
                height: 10px;
                background: lightgray;
            }

            QSlider::handle:horizontal {
                background: red;
                border: 1px;
                width: 5px;
                margin: -5px 0;
                border-radius: 2px;
            }

            QSlider::sub-page:horizontal {
                background: purple;
            }""")
            self.easter_egg_color_nbr += 1
        elif self.easter_egg_color_nbr == 6:
            self.lb_title.setStyleSheet("QLabel { color : pink; }")
            self.list.setStyleSheet("QListWidget::item { color : pink; }")
            self.time_bar.setStyleSheet("""QSlider::groove:horizontal {
                border: 1px;
                height: 10px;
                background: lightgray;
            }

            QSlider::handle:horizontal {
                background: red;
                border: 1px;
                width: 5px;
                margin: -5px 0;
                border-radius: 2px;
            }

            QSlider::sub-page:horizontal {
                background: pink;
            }""")
            self.sl_volume.setStyleSheet("""QSlider::groove:horizontal {
                border: 1px;
                height: 10px;
                background: lightgray;
            }

            QSlider::handle:horizontal {
                background: red;
                border: 1px;
                width: 5px;
                margin: -5px 0;
                border-radius: 2px;
            }

            QSlider::sub-page:horizontal {
                background: pink;
            }""")
            self.easter_egg_color_nbr += 1
        elif self.easter_egg_color_nbr == 7:
            self.lb_title.setStyleSheet("QLabel { color : brown; }")
            self.list.setStyleSheet("QListWidget::item { color : brown; }")
            self.time_bar.setStyleSheet("""QSlider::groove:horizontal {
                border: 1px;
                height: 10px;
                background: lightgray;
            }

            QSlider::handle:horizontal {
                background: red;
                border: 1px;
                width: 5px;
                margin: -5px 0;
                border-radius: 2px;
            }

            QSlider::sub-page:horizontal {
                background: brown;
            }""")
            self.sl_volume.setStyleSheet("""QSlider::groove:horizontal {
                border: 1px;
                height: 10px;
                background: lightgray;
            }

            QSlider::handle:horizontal {
                background: red;
                border: 1px;
                width: 5px;
                margin: -5px 0;
                border-radius: 2px;
            }

            QSlider::sub-page:horizontal {
                background: brown;
            }""")
            self.easter_egg_color_nbr += 1
        elif self.easter_egg_color_nbr == 8:
            self.lb_title.setStyleSheet("QLabel { color : white; }")
            self.list.setStyleSheet("QListWidget::item { color : white; }")
            self.time_bar.setStyleSheet("""QSlider::groove:horizontal {
                border: 1px;
                height: 10px;
                background: lightgray;
            }

            QSlider::handle:horizontal {
                background: red;
                border: 1px;
                width: 5px;
                margin: -5px 0;
                border-radius: 2px;
            }

            QSlider::sub-page:horizontal {
                background: white;
            }""")
            self.sl_volume.setStyleSheet("""QSlider::groove:horizontal {
                border: 1px;
                height: 10px;
                background: lightgray;
            }

            QSlider::handle:horizontal {
                background: red;
                border: 1px;
                width: 5px;
                margin: -5px 0;
                border-radius: 2px;
            }

            QSlider::sub-page:horizontal {
                background: white;
            }""")
            self.easter_egg_color_nbr += 1
        elif self.easter_egg_color_nbr == 9:
            self.lb_title.setStyleSheet("QLabel { color : gray; }")
            self.list.setStyleSheet("QListWidget::item { color : gray; }")
            self.time_bar.setStyleSheet("""QSlider::groove:horizontal {
                border: 1px;
                height: 10px;
                background: lightgray;
            }

            QSlider::handle:horizontal {
                background: red;
                border: 1px;
                width: 5px;
                margin: -5px 0;
                border-radius: 2px;
            }

            QSlider::sub-page:horizontal {
                background: gray;
            }""")
            self.sl_volume.setStyleSheet("""QSlider::groove:horizontal {
                border: 1px;
                height: 10px;
                background: lightgray;
            }

            QSlider::handle:horizontal {
                background: red;
                border: 1px;
                width: 5px;
                margin: -5px 0;
                border-radius: 2px;
            }

            QSlider::sub-page:horizontal {
                background: gray;
            }""")
            self.easter_egg_color_nbr += 1
        elif self.easter_egg_color_nbr == 10:
            self.lb_title.setStyleSheet("QLabel { color : black; }")
            self.list.setStyleSheet("QListWidget::item { color : black; }")
            self.time_bar.setStyleSheet("""QSlider::groove:horizontal {
                border: 1px;
                height: 10px;
                background: lightgray;
            }

            QSlider::handle:horizontal {
                background: red;
                border: 1px;
                width: 5px;
                margin: -5px 0;
                border-radius: 2px;
            }

            QSlider::sub-page:horizontal {
                background: black;
            }""")
            self.sl_volume.setStyleSheet("""QSlider::groove:horizontal {
                border: 1px;
                height: 10px;
                background: lightgray;
            }

            QSlider::handle:horizontal {
                background: red;
                border: 1px;
                width: 5px;
                margin: -5px 0;
                border-radius: 2px;
            }

            QSlider::sub-page:horizontal {
                background: black;
            }""")
            self.easter_egg_color_nbr = 0

    def eventFilter(self, watched: QtCore.QObject, event: QtCore.QEvent) -> bool:
        if watched == self.lb_img_volume and event.type() == QtCore.QEvent.Enter:
            self.main_layout.removeWidget(self.lb_img_volume)
            self.main_layout.removeWidget(self.time_bar)

            self.main_layout.addWidget(self.lb_volume, 5, 18, 1, 1)
            self.main_layout.addWidget(self.sl_volume, 5, 16, 1, 2)
            self.main_layout.addWidget(self.lb_img_volume, 5, 15, 1, 1)
            self.main_layout.addWidget(self.time_bar, 5, 5, 1, 10)

            self.sl_volume.setHidden(False)
            self.lb_volume.setHidden(False)
        elif watched == self.sl_volume and event.type() == QtCore.QEvent.Leave:
            self.main_layout.removeWidget(self.lb_volume)
            self.main_layout.removeWidget(self.sl_volume)
            self.main_layout.removeWidget(self.lb_img_volume)
            self.main_layout.removeWidget(self.time_bar)

            self.main_layout.addWidget(self.lb_img_volume, 5, 18, 1, 1)
            self.main_layout.addWidget(self.time_bar, 5, 5, 1, 13)

            self.sl_volume.setHidden(True)
            self.lb_volume.setHidden(True)
        return super().eventFilter(watched, event)

    def get_musics(self):
        self.files = glob(os.path.join(self.settings["folder"], "*.mp3"))
        self.filelist = []
        for self.file in self.files:
            try:
                self.tag = eyed3.load(self.file).tag
            except:
                self.error = QtWidgets.QMessageBox()
                self.error.setWindowTitle("Error!")
                self.error.setText("Error 0X0001: Can't read properties!")
                self.error.setInformativeText("Attempted reading ''Title'' and ''Artist'' properties as them not being "
                                              "registered in file.\nConsider adding them.")
                self.error.exec_()
            self.filelist.append(f"{self.tag.title} | {self.tag.artist}")
        self.list.addItems(self.filelist)
        self.nbr = 0

    def help(self):
        self.help_win = Help(self.appctxt)
        self.help_win.show()

    def max(self):
        if not self.isFullScreen():
            if self.isMaximized():
                self.set_btn_icon([self.btn_max], [self.appctxt.get_resource("maximize.png")])
                self.showNormal()
                self.setFixedSize(650, 350)
                self.move(self.rectangle.topLeft())
            else:
                self.set_btn_icon([self.btn_max], [self.appctxt.get_resource("minimise.png")])
                self.showMaximized()
        else:
            self.set_btn_icon([self.btn_max], [self.appctxt.get_resource("maximize.png")])
            self.showNormal()

    def modify_details(self):
        self.details = ModifyDetails(self.files[self.list.currentRow()], self)
        self.details.show()
        self.stop()

    def next(self):
        self.nbr = self.list.currentRow() + 1
        if not self.list.count() == self.nbr:
            self.list.setCurrentRow(self.list.currentRow() + 1)
        else:
            self.list.setCurrentRow(0)
            self.nbr = 0
        self.read_file()

    def open_settings(self):
        if not os.path.exists(os.path.join(self.cur_dir, "A+Music/settings.json")):
            os.makedirs(os.path.join(self.cur_dir, "A+Music/"))
            with open(os.path.join(self.cur_dir, "A+Music/settings.json"), "w") as a:
                self.settings = {"folder": "C:/Users/pc/Music", "volume": 100, "easter_egg_on": False, "configured": False}
                json.dump(self.settings, a)
        with open(os.path.join(self.cur_dir, "A+Music/settings.json"), "r") as f:
            self.settings = json.load(f)
            f.close()
        self.sl_volume.setValue(self.settings["volume"])
        if self.settings["easter_egg_on"] == True:
            self.settings["easter_egg_on"] = False
            self.easter_egg()

    def play(self, path):
        self.sound = QtMultimedia.QMediaPlayer()
        self.media = QtCore.QUrl.fromLocalFile(path)
        self.file = QtMultimedia.QMediaContent(self.media)
        self.sound.setMedia(self.file)
        self.set_btn_icon([self.btn_play], [self.appctxt.get_resource("pause.png")])
        self.a, self.b, self.c = 0, 0, 0
        self.timer(1000, False, self.play_bar_n_lb)
        self.sound.play()
        self.refresh_volume()

    def play_bar_n_lb(self):
        self.minutes = int(self.sound.duration() / 1000 / 60)
        self.seconds = int(self.sound.duration() / 1000 % 60)
        self.time_bar.setRange(0, int(self.sound.duration() / 1000))
        if self.sound.state() == self.sound.state().PlayingState:
            if not self.a == 59:
                self.a += 1
            else:
                self.b += 1
                self.a = 0
            self.c += 1
            self.lb_time.setText(f"{self.b}:{self.a} / {self.minutes}:{self.seconds}")
            self.time_bar.setValue(self.c)
        if self.c == int(self.sound.duration() / 1000):
            self.next()

    def play_pause(self):
        if self.sound.state() == self.sound.state().PlayingState:
            self.sound.pause()
            if self.sound.state() == self.sound.state().PausedState:
                pass
                self.set_btn_icon([self.btn_play], [self.appctxt.get_resource("play.png")])
        elif self.sound.state() == self.sound.state().PausedState:
            self.sound.play()
            if self.sound.state() == self.sound.state().PlayingState:
                pass
                self.set_btn_icon([self.btn_play], [self.appctxt.get_resource("pause.png")])

    def quicksetup(self):
        if self.settings["configured"] == False:
            self.dialog = Wizard(self.cur_dir)
            self.dialog.exec_()
            self.open_settings()
        else:
            pass

    def read_file(self):
        self.selected = self.list.currentRow()
        self.a = self.files[self.selected]
        self.play(self.a)

    def refresh(self):
        self.list.clear()
        self.get_musics()

    def refresh_volume(self):
        try:
            self.sound.setVolume(self.settings["volume"])
        except:
            pass

    def save_settings(self):
        with open(os.path.join(self.cur_dir, "A+Music/settings.json"), "w") as c:
            json.dump(self.settings, c)

    def set_btn_icon(self, btn_list, icon_path_list):
        a = 0
        for btn in btn_list:
            btn.setIcon(QtGui.QIcon(icon_path_list[a]))
            a += 1

    def set_btn_size(self, btn_list, H, V):
        for btn in btn_list:
            btn.setFixedSize(H, V)

    def set_btn_flat(self, btn_list, cond):
        for btn in btn_list:
            btn.setFlat(cond)

    def set_folder(self):
        self.ask = QtWidgets.QFileDialog()
        self.ask.setFileMode(self.ask.Directory)
        self.music_dir = self.ask.getExistingDirectory()
        self.settings["folder"] = self.music_dir
        self.save_settings()
        self.refresh()

    def set_time(self):
        self.sound.setPosition(self.time_bar.value() * 1000)
        self.c = self.time_bar.value()
        self.b = int(self.time_bar.value() / 60)
        self.a = self.time_bar.value() % 60

    def settings_menu(self):
        self.setts.addAction(QtGui.QIcon(self.appctxt.get_resource("about.png")), "About", self.about,
                             QtGui.QKeySequence("f10"))
        self.setts.addAction(QtGui.QIcon(self.appctxt.get_resource("help.png")), "Help", self.help,
                             QtGui.QKeySequence("f1"))
        self.setts.addAction(QtGui.QIcon(self.appctxt.get_resource("refresh.png")), "Refresh The List", self.refresh,
                             QtGui.QKeySequence("f5"))
        self.setts.addAction(QtGui.QIcon(self.appctxt.get_resource("folder.png")), "Set The Music Folder",
                             self.set_folder, QtGui.QKeySequence("f2"))

    def set_volume(self):
        self.settings["volume"] = self.sl_volume.value()
        self.lb_volume.setText(f"{self.sl_volume.value()}%")
        if self.sl_volume.value() >= 75:
            self.sl_volume.setStyleSheet("""QSlider::groove:horizontal {
    border: 1px;
    height: 10px;
    background: lightgray;
}

QSlider::handle:horizontal {
    background: red;
    border: 1px;
    width: 5px;
    margin: -5px 0;
    border-radius: 2px;
}

QSlider::sub-page:horizontal {
    background: orange;
}""")
            self.lb_volume.setStyleSheet("QLabel { color : orange; }")
        elif self.sl_volume.value() < 75:
            self.sl_volume.setStyleSheet("""QSlider::groove:horizontal {
                border: 1px;
                height: 10px;
                background: lightgray;
            }

            QSlider::handle:horizontal {
                background: red;
                border: 1px;
                width: 5px;
                margin: -5px 0;
                border-radius: 2px;
            }

            QSlider::sub-page:horizontal {
                background: lightblue;
            }""")
            self.lb_volume.setStyleSheet("QLabel { color : default; }")
        self.save_settings()
        self.refresh_volume()

    def showhide(self):
        if self.isHidden():
            self.showNormal()
        else:
            self.hide()

    def stop(self):
        self.sound.stop()
        self.time_bar.setValue(0)
        self.lb_time.setText("0:0 / 0:0")
        self.set_btn_icon([self.btn_play], [self.appctxt.get_resource("play.png")])
        self.timer_.stop()
        self.media.clear()
        self.file = QtMultimedia.QMediaContent(self.media)
        self.sound.setMedia(self.file)

    def timer(self, interval, singleshot, method):
        self.timer_ = QtCore.QTimer()
        self.timer_.setInterval(interval)
        self.timer_.setSingleShot(singleshot)
        self.timer_.timeout.connect(method)
        self.timer_.start()


class Help(QtWidgets.QWidget):

    def __init__(self, appctxt):
        super().__init__()
        self.setWindowTitle("A+Music | Help")
        self.setFixedSize(320, 350)
        self.rectangle = self.frameGeometry()
        self.centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        self.rectangle.moveCenter(self.centerPoint)
        self.move(self.rectangle.topLeft())
        self.appctxt = appctxt
        self.setup_ui()

    def setup_ui(self):
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.settings_menu()
        self.setup_connections()

    #  Ui--------------------------------------------------------

    def create_widgets(self):
        self.time_bar = QtWidgets.QSlider()
        self.lb_time_bar = QtWidgets.QLabel("Slide to move position in the song.")
        self.list = QtWidgets.QListWidget()
        self.lb_list = QtWidgets.QLabel("Click on an item to play it.\nDouble-click to edit.")
        self.setts = QtWidgets.QMenu()
        self.btn_setts = QtWidgets.QPushButton()
        self.lb_btn_setts = QtWidgets.QLabel("Click to show the menu.")
        self.sl_volume = QtWidgets.QSlider()
        self.lb_sl_volume = QtWidgets.QLabel("Slide to change the volume.")
        self.btn_play = QtWidgets.QPushButton()
        self.lb_btn_play = QtWidgets.QLabel("Click to play/pause the current playing song.")
        self.btn_next = QtWidgets.QPushButton()
        self.lb_btn_next = QtWidgets.QLabel("Click to play the next song.")
        self.btn_back = QtWidgets.QPushButton()
        self.lb_btn_back = QtWidgets.QLabel("Click to play the last song.")
        self.btn_stop = QtWidgets.QPushButton()
        self.lb_btn_stop =QtWidgets.QLabel("Click to stop the current playing song.")
        self.btn_ok = QtWidgets.QPushButton("Ok")
        self.output = QtWidgets.QLabel("Output: None")

    def modify_widgets(self):
        self.output.setAlignment(QtCore.Qt.AlignCenter)
        self.btn_ok.setDefault(True)
        self.set_btn_size([self.btn_play,
                           self.btn_next,
                           self.btn_back,
                           self.btn_stop], 25, 25)
        self.set_btn_flat([self.btn_play,
                           self.btn_next,
                           self.btn_back,
                           self.btn_stop,
                           self.btn_setts,], True)
        self.set_btn_icon([self.btn_play,
                           self.btn_next,
                           self.btn_back,
                           self.btn_stop,
                           self.btn_setts],
                          [self.appctxt.get_resource("play.png"),
                           self.appctxt.get_resource("next.png"),
                           self.appctxt.get_resource("back.png"),
                           self.appctxt.get_resource("stop.png"),
                           self.appctxt.get_resource("more.png")])
        self.time_bar.setOrientation(QtCore.Qt.Horizontal)
        self.btn_setts.setMenu(self.setts)
        self.btn_setts.setFixedSize(45, 25)
        self.time_bar.setStyleSheet("""QSlider::groove:horizontal {
            border: 1px;
            height: 10px;
            background: lightgray;
        }

        QSlider::handle:horizontal {
            background: red;
            border: 1px;
            width: 5px;
            margin: -5px 0;
            border-radius: 2px;
        }

        QSlider::sub-page:horizontal {
            background: lightblue;
        }""")
        self.sl_volume.setPageStep(1)
        self.sl_volume.setOrientation(QtCore.Qt.Horizontal)
        self.sl_volume.setStyleSheet("""QSlider::groove:horizontal {
            border: 1px;
            height: 10px;
            background: lightgray;
        }

        QSlider::handle:horizontal {
            background: red;
            border: 1px;
            width: 5px;
            margin: -5px 0;
            border-radius: 2px;
        }

        QSlider::sub-page:horizontal {
            background: lightblue;
        }""")
        self.sl_volume.setRange(0, 100)
        self.list.addItems(["Test N°1", "Test N°2", "Test N°3"])
        self.list.setFixedWidth(75)
        self.time_bar.setFixedWidth(75)
        self.sl_volume.setFixedWidth(75)

    def create_layouts(self):
        self.main_layout = QtWidgets.QGridLayout(self)

    def add_widgets_to_layouts(self):
        self.main_layout.addWidget(self.list, 1, 1)
        self.main_layout.addWidget(self.lb_list, 1, 2)
        self.main_layout.addWidget(self.time_bar, 2, 1)
        self.main_layout.addWidget(self.lb_time_bar, 2, 2)
        self.main_layout.addWidget(self.sl_volume, 3, 1)
        self.main_layout.addWidget(self.lb_sl_volume, 3, 2)
        self.main_layout.addWidget(self.btn_play, 4, 1)
        self.main_layout.addWidget(self.lb_btn_play, 4, 2)
        self.main_layout.addWidget(self.btn_next, 5, 1)
        self.main_layout.addWidget(self.lb_btn_next, 5, 2)
        self.main_layout.addWidget(self.btn_back, 6, 1)
        self.main_layout.addWidget(self.lb_btn_back, 6, 2)
        self.main_layout.addWidget(self.btn_stop, 7, 1)
        self.main_layout.addWidget(self.lb_btn_stop, 7, 2)
        self.main_layout.addWidget(self.btn_setts, 8, 1)
        self.main_layout.addWidget(self.lb_btn_setts, 8, 2)
        self.main_layout.addWidget(self.output, 9, 1, 1, 2)

    def setup_connections(self):
        self.btn_ok.clicked.connect(self.close)
        self.list.itemClicked.connect(self.list_single)
        self.list.itemDoubleClicked.connect(self.list_double)
        self.btn_play.clicked.connect(self.play)
        self.btn_stop.clicked.connect(self.stop)
        self.time_bar.valueChanged.connect(self.time)
        self.btn_next.clicked.connect(self.next)
        self.btn_back.clicked.connect(self.back)
        self.sl_volume.valueChanged.connect(self.volume)

    #   Methods---------------------------------------------------

    def set_btn_icon(self, btn_list, icon_path_list):
        a = 0
        for btn in btn_list:
            btn.setIcon(QtGui.QIcon(icon_path_list[a]))
            a += 1

    def set_btn_size(self, btn_list, H, V):
        for btn in btn_list:
            btn.setFixedSize(H, V)

    def set_btn_flat(self, btn_list, cond):
        for btn in btn_list:
            btn.setFlat(cond)

    def settings_menu(self):
        self.setts.addAction(QtGui.QIcon(self.appctxt.get_resource("about.png")), "About", self.about,
                             QtGui.QKeySequence("f10"))
        self.setts.addAction(QtGui.QIcon(self.appctxt.get_resource("help.png")), "Help", self.help,
                             QtGui.QKeySequence("f1"))
        self.setts.addAction(QtGui.QIcon(self.appctxt.get_resource("refresh.png")), "Refresh The List", self.refresh,
                             QtGui.QKeySequence("f5"))
        self.setts.addAction(QtGui.QIcon(self.appctxt.get_resource("folder.png")), "Set The Music Folder",
                             self.folder, QtGui.QKeySequence("f2"))

    #   Output----------------------------------------------------

    def about(self):
        self.output.setText("Output: About opened.")

    def list_single(self):
        self.output.setText("Output: Playing song.")

    def list_double(self):
        self.output.setText("Output: Edit Item Window opened")

    def time(self):
        self.output.setText("Output: Song current position changed.")

    def volume(self):
        self.output.setText("Output: Volume changed.")

    def play(self):
        self.output.setText("Output: Playing/Pausing the current song.")

    def next(self):
        self.output.setText("Output: Playing next song.")

    def back(self):
        self.output.setText("Output: Playing last song.")

    def stop(self):
        self.output.setText("Output: Stopping the current song.")

    def help(self):
        self.output.setText("Output: Help opened.")

    def folder(self):
        self.output.setText("Output: Set Folder opened.")

    def refresh(self):
        self.output.setText("Output: Refreshed the list.")


class ModifyDetails(QtWidgets.QWidget):

    def __init__(self, file, mainwindow):
        super().__init__()
        self.file = file
        self.mainwindow = mainwindow
        self.setup_ui()

    def setup_ui(self):
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layout()
        self.setup_connections()

    #   Ui--------------------------------------------------------

    def create_widgets(self):
        self.btn_ok = QtWidgets.QPushButton("Ok")
        self.le_title = QtWidgets.QLineEdit()
        self.le_artist = QtWidgets.QLineEdit()
        self.lb_text = QtWidgets.QLabel("Define the Title and/or the Artist.")
        self.lb_title = QtWidgets.QLabel("Title:")
        self.lb_artist = QtWidgets.QLabel("Artist:")

    def modify_widgets(self):
        self.tag = eyed3.load(self.file).tag
        self.le_title.setText(self.tag.title)
        self.le_artist.setText(self.tag.artist)

    def create_layouts(self):
        self.main_layout = QtWidgets.QGridLayout(self)

    def add_widgets_to_layout(self):
        self.main_layout.addWidget(self.lb_text, 1, 1, 1, 3)
        self.main_layout.addWidget(self.le_title, 2, 2, 1, 2)
        self.main_layout.addWidget(self.lb_title, 2, 1, 1, 1)
        self.main_layout.addWidget(self.lb_artist, 3, 1, 1, 1)
        self.main_layout.addWidget(self.le_artist, 3, 2, 1, 2)
        self.main_layout.addWidget(self.btn_ok, 4, 3, 1, 1)

    def setup_connections(self):
        self.btn_ok.clicked.connect(self.save_details)

    #   Methods---------------------------------------------------

    def save_details(self):
        self.tag.artist = self.le_artist.text()
        self.tag.title = self.le_title.text()
        self.tag.save()
        self.close()
        MainWindow.refresh(self.mainwindow)


class Wizard(QtWidgets.QWizard):

    def __init__(self, cur_dir):
        super().__init__()
        self.cur_dir = cur_dir
        self.setup_pages()

    def setup_pages(self):
        self.open_settings()
        self.page1()
        self.page2()
        self.page3()
        self.add_pages()
        self.save_settings()

    #   Ui--------------------------------------------------------

    def page1(self):
        self.page1 = QtWidgets.QWizardPage()
        self.page1.setTitle("Quick Setup")
        self.page1.setSubTitle("This is the First Time setup.\nIt will help you configure the app.")

    def page2(self):
        self.page2 = QtWidgets.QWizardPage()
        self.page2.setTitle("Quick Setup")
        self.page2.setSubTitle("Set default values.")
        self.page2_btn = QtWidgets.QPushButton("Open Directory")
        self.page2_lb = QtWidgets.QLabel("C:/Users/pc/Music")
        self.page2_lb_vol = QtWidgets.QLabel("Volume:")
        self.page2_lb_vol_perc = QtWidgets.QLabel("100%")
        self.page2_sl = QtWidgets.QSlider()
        self.page2_sl.setRange(0, 100)
        self.page2_sl.setValue(100)
        self.page2_sl.setOrientation(QtCore.Qt.Horizontal)
        self.page2_sl.setStyleSheet("""QSlider::groove:horizontal {
            border: 1px;
            height: 10px;
            background: lightgray;
        }

        QSlider::handle:horizontal {
            background: red;
            border: 1px;
            width: 5px;
            margin: -5px 0;
            border-radius: 2px;
        }

        QSlider::sub-page:horizontal {
            background: lightblue;
        }""")
        self.page2_layout = QtWidgets.QGridLayout(self.page2)
        self.page2_layout.addWidget(self.page2_btn, 1, 4)
        self.page2_layout.addWidget(self.page2_lb, 1, 1, 1, 3)
        self.page2_layout.addWidget(self.page2_sl, 2, 3)
        self.page2_layout.addWidget(self.page2_lb_vol, 2, 1)
        self.page2_layout.addWidget(self.page2_lb_vol_perc, 2, 4)
        self.page2_btn.clicked.connect(self.page2_set_folder)
        self.page2_sl.valueChanged.connect(self.page2_set_volume)

    def page3(self):
        self.page3 = QtWidgets.QWizardPage()
        self.page3.setTitle("Quick Setup")
        self.page3.setSubTitle("Done!\nThe app is now ready to go!")

    def add_pages(self):
        self.addPage(self.page1)
        self.addPage(self.page2)
        self.addPage(self.page3)

    #   Methods---------------------------------------------------

    def open_settings(self):
        with open(os.path.join(self.cur_dir, "A+Music/settings.json"), "r") as f:
            self.settings = json.load(f)
            self.settings["folder"] = "C:/Users/pc/Music"
            self.settings["volume"] = 100
            self.settings["easter_egg_on"] = False
            f.close()

    def page2_set_folder(self):
        self.ask = QtWidgets.QFileDialog()
        self.ask.setFileMode(self.ask.Directory)
        self.settings["folder"] = self.ask.getExistingDirectory()
        self.page2_lb.setText(self.settings["folder"])
        self.save_settings()

    def page2_set_volume(self):
        self.page2_lb_vol_perc.setText(str(self.page2_sl.value()) + "%")
        self.settings["volume"] = self.page2_sl.value()
        self.save_settings()

    def save_settings(self):
        self.settings["configured"] = True
        with open(os.path.join(self.cur_dir, "A+Music/settings.json"), "w") as c:
            json.dump(self.settings, c)
