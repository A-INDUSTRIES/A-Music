from PySide2 import QtWidgets, QtCore, QtGui, QtMultimedia
from glob import glob

from help_window import Help
from details_window import ModifyDetails
from wizard_window import Wizard

import os, json, eyed3, logging

cur_dir = os.path.join(os.path.expanduser("~"), "A+Music") #Gets the folder where setting file is gonna be.

log_file = os.path.join(cur_dir, "latest_log.txt")

logging.basicConfig(level=logging.INFO, filename=log_file, filemode="w",
                    format='%(asctime)s | %(levelname)s - %(message)s') #Configuring logging system.

class MainWindow(QtWidgets.QWidget):

    def __init__(self, appctxt):
        super().__init__()
        self.appctxt = appctxt
        logging.info("Initialized Logging.")
        self.resize(650, 350)
        logging.info("Resizing MainWindow.")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        logging.info("Set MainWindow Frameless.")
        self.rectangle = self.frameGeometry()
        self.centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        self.rectangle.moveCenter(self.centerPoint)
        self.move(self.rectangle.topLeft())
        logging.info("Moved window to center of screen.")
        logging.info("Setting up the ui.")
        self.setup_ui()

    def setup_ui(self):
        logging.info("Creating Widgets...")
        self.create_widgets()
        logging.info("Creating System Tray...")
        self.create_sys_tray_icon()
        logging.info("Modifying Widgets...")
        self.modify_widgets()
        logging.info("Creating Layout...")
        self.create_layouts()
        logging.info("Adding Widgets to Layout...")
        self.add_widgets_to_layouts()
        logging.info("Setting Connections...")
        self.setup_connections()
        logging.info("Opening Settings.")
        self.open_settings()
        logging.info("Setting the Menu.")
        self.settings_menu()
        logging.info("Making Wizard if First Time.")
        self.wizard()
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

        self.sg_resize = QtWidgets.QSizeGrip(self)

    def create_sys_tray_icon(self):
        """Create the taskbar icon with menu."""
        self.tray = QtWidgets.QSystemTrayIcon()
        self.tray.setIcon(QtGui.QIcon(self.appctxt.get_resource("icon.png")))
        self.tray.setVisible(True)
        self.tray_menu = QtWidgets.QMenu()
        self.tray_menu.addAction(QtGui.QIcon(self.appctxt.get_resource("play.png")), "Play/Pause", self.play_pause)
        self.tray_menu.addAction(QtGui.QIcon(self.appctxt.get_resource("next.png")), "Next", self.next)
        self.tray_menu.addAction(QtGui.QIcon(self.appctxt.get_resource("back.png")), "Previous", self.back)
        self.tray_menu.addAction(QtGui.QIcon(self.appctxt.get_resource("stop.png")), "Stop", self.stop)
        self.tray_menu.addAction(QtGui.QIcon(self.appctxt.get_resource("close.png")), "Show/Hide", self.show_hide)
        self.tray.setContextMenu(self.tray_menu)

    def modify_widgets(self):
        """Setting different atributes to widgets.
        Example: Setting StyleSheet, Setting btn size, Setting btn image, etc..."""
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
        self.set_sliders_stylesheet("lightblue", [self.time_bar])

        self.list.setDragEnabled(False)

        self.btn_setts.setMenu(self.setts)
        self.btn_setts.setFixedSize(45, 25)

        self.sl_volume.installEventFilter(self)
        self.sl_volume.setMouseTracking(True)
        self.sl_volume.setPageStep(1)
        self.sl_volume.setOrientation(QtCore.Qt.Horizontal)
        self.set_sliders_stylesheet("lightblue", [self.sl_volume])
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
        self.main_layout.addWidget(self.btn_close, 1, 22, 1, 1)
        self.main_layout.addWidget(self.btn_max, 1, 21, 1, 1)
        self.main_layout.addWidget(self.btn_min, 1, 20, 1, 1)
        self.main_layout.addWidget(self.lb_title, 1, 1, 2, 11)
        self.main_layout.addWidget(self.lb_time, 5, 19, 1, 3)
        self.main_layout.addWidget(self.sg_resize, 5, 22, 1, 1, QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)
        self.main_layout.addWidget(self.btn_play, 5, 2, 1, 1)
        self.main_layout.addWidget(self.btn_back, 5, 1, 1, 1)
        self.main_layout.addWidget(self.btn_next, 5, 3, 1, 1)
        self.main_layout.addWidget(self.btn_stop, 5, 4, 1, 1)
        self.main_layout.addWidget(self.list, 3, 1, 1, 22)
        self.main_layout.addWidget(self.btn_setts, 1, 19, 1, 1)
        self.main_layout.addWidget(self.lb_img_volume, 5, 18, 1, 1)
        self.main_layout.addWidget(self.time_bar, 5, 5, 1, 13)
        self.main_layout.addWidget(self.btn_easter_egg, 1, 1, 2, 1)

    def setup_connections(self):
        self.btn_close.clicked.connect(self.close)
        self.btn_max.clicked.connect(self.max)
        self.btn_min.clicked.connect(self.showMinimized)
        self.list.itemClicked.connect(self.play)
        self.list.itemDoubleClicked.connect(self.modify_details)
        self.btn_play.clicked.connect(self.play_pause)
        self.btn_stop.clicked.connect(self.stop)
        self.time_bar.sliderMoved.connect(self.set_time)
        self.btn_next.clicked.connect(self.next)
        self.btn_back.clicked.connect(self.back)
        self.btn_easter_egg.clicked.connect(self.easter_egg)
        self.sl_volume.valueChanged.connect(self.set_volume)

    #  Methods---------------------------------------------------

    def about(self):
        """Creating About window containing info about the app."""
        logging.info("Opened ''About''")
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
        logging.info("Playing last track.")
        self.nbr = self.list.currentRow() - 1
        if not self.nbr == -1:
            self.list.setCurrentRow(self.list.currentRow() - 1)
        else:
            self.list.setCurrentRow(self.list.count() - 1)
            self.nbr = self.list.count() - 1
        self.play()

    def closeEvent(self, event: QtGui.QCloseEvent):
        """Making sure everything is saved before process ends."""
        logging.info("Saving settings before closing.")
        self.save_settings()

    def easter_egg(self):
        """Turning on/off easter egg."""
        if self.settings["easter_egg_on"] == False:
            self.easter_egg_timer = QtCore.QTimer()
            self.easter_egg_timer.setInterval(100)
            self.easter_egg_timer.timeout.connect(self.easter_egg_animate)
            self.easter_egg_color_nbr = 0
            self.easter_egg_timer.start()
            self.settings["easter_egg_on"] = True
            self.save_settings()
            logging.info("Easter Egg Activated!")
        elif self.settings["easter_egg_on"] == True:
            self.easter_egg_timer.stop()
            self.lb_title.setStyleSheet("QLabel { color : red; }")
            self.list.setStyleSheet("QListWidget::item { color : black; }")
            self.set_volume()
            self.set_sliders_stylesheet("lightblue", [self.time_bar])
            self.settings["easter_egg_on"] = False
            self.save_settings()
            logging.info("Easter Egg Off.")

    def easter_egg_animate(self):
        """Child of 'easter_egg'. DO NOT USE APPART!
        For each loop, it sets the stylesheet of list, btns, etc to another colour."""
        if self.easter_egg_color_nbr == 0:
            self.lb_title.setStyleSheet("QLabel { color : red; }")
            self.list.setStyleSheet("QListWidget::item { color : red; }")
            self.set_sliders_stylesheet("red", [self.time_bar, self.sl_volume])
            self.easter_egg_color_nbr += 1
        elif self.easter_egg_color_nbr == 1:
            self.lb_title.setStyleSheet("QLabel { color : orange; }")
            self.list.setStyleSheet("QListWidget::item { color : orange; }")
            self.set_sliders_stylesheet("orange", [self.time_bar, self.sl_volume])
            self.easter_egg_color_nbr += 1
        elif self.easter_egg_color_nbr == 2:
            self.lb_title.setStyleSheet("QLabel { color : yellow; }")
            self.list.setStyleSheet("QListWidget::item { color : yellow; }")
            self.set_sliders_stylesheet("yellow", [self.time_bar, self.sl_volume])
            self.easter_egg_color_nbr += 1
        elif self.easter_egg_color_nbr == 3:
            self.lb_title.setStyleSheet("QLabel { color : green; }")
            self.list.setStyleSheet("QListWidget::item { color : green; }")
            self.set_sliders_stylesheet("green", [self.time_bar, self.sl_volume])
            self.easter_egg_color_nbr += 1
        elif self.easter_egg_color_nbr == 4:
            self.lb_title.setStyleSheet("QLabel { color : blue; }")
            self.list.setStyleSheet("QListWidget::item { color : blue; }")
            self.set_sliders_stylesheet("blue", [self.time_bar, self.sl_volume])
            self.easter_egg_color_nbr += 1
        elif self.easter_egg_color_nbr == 5:
            self.lb_title.setStyleSheet("QLabel { color : purple; }")
            self.list.setStyleSheet("QListWidget::item { color : purple; }")
            self.set_sliders_stylesheet("purple", [self.time_bar, self.sl_volume])
            self.easter_egg_color_nbr += 1
        elif self.easter_egg_color_nbr == 6:
            self.lb_title.setStyleSheet("QLabel { color : pink; }")
            self.list.setStyleSheet("QListWidget::item { color : pink; }")
            self.set_sliders_stylesheet("pink", [self.time_bar, self.sl_volume])
            self.easter_egg_color_nbr += 1
        elif self.easter_egg_color_nbr == 7:
            self.lb_title.setStyleSheet("QLabel { color : brown; }")
            self.list.setStyleSheet("QListWidget::item { color : brown; }")
            self.set_sliders_stylesheet("brown", [self.time_bar, self.sl_volume])
            self.easter_egg_color_nbr += 1
        elif self.easter_egg_color_nbr == 8:
            self.lb_title.setStyleSheet("QLabel { color : white; }")
            self.list.setStyleSheet("QListWidget::item { color : white; }")
            self.set_sliders_stylesheet("white", [self.time_bar, self.sl_volume])
            self.easter_egg_color_nbr += 1
        elif self.easter_egg_color_nbr == 9:
            self.lb_title.setStyleSheet("QLabel { color : gray; }")
            self.list.setStyleSheet("QListWidget::item { color : gray; }")
            self.set_sliders_stylesheet("gray", [self.time_bar, self.sl_volume])
            self.easter_egg_color_nbr += 1
        elif self.easter_egg_color_nbr == 10:
            self.lb_title.setStyleSheet("QLabel { color : black; }")
            self.list.setStyleSheet("QListWidget::item { color : black; }")
            self.set_sliders_stylesheet("black", [self.time_bar, self.sl_volume])
            self.easter_egg_color_nbr = 0

    def eventFilter(self, watched: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """Showing volume bar if label hovered. Hiding if unhovered."""
        if watched == self.lb_img_volume and event.type() == QtCore.QEvent.Enter:
            logging.info("Showing Volume Bar...")
            self.main_layout.removeWidget(self.lb_img_volume)
            self.main_layout.removeWidget(self.time_bar)

            self.main_layout.addWidget(self.lb_volume, 5, 18, 1, 1)
            self.main_layout.addWidget(self.sl_volume, 5, 16, 1, 2)
            self.main_layout.addWidget(self.lb_img_volume, 5, 15, 1, 1)
            self.main_layout.addWidget(self.time_bar, 5, 5, 1, 10)

            self.sl_volume.setHidden(False)
            self.lb_volume.setHidden(False)
        elif watched == self.sl_volume and event.type() == QtCore.QEvent.Leave:
            logging.info("Hiding Volume Bar...")
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
        """Searching user defined folder to find all .mp3 files and adding them to the list."""
        logging.info("Getting Musics.")
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
            if not self.tag.title == None and not self.tag.artist == None:
                self.filelist.append(f"{self.tag.title} | {self.tag.artist}")
            else:
                self.filelist.append(f"{self.tag.title} | {self.tag.artist} ~{os.path.basename(self.file)}")
        self.list.addItems(self.filelist)
        self.nbr = 0

    def help(self):
        """Obviously... It opens help."""
        logging.info("Opened Help.")
        self.help_win = Help(self.appctxt)
        self.help_win.show()

    def max(self):
        """Maximizing or minimizing window based on current state."""
        if not self.isFullScreen():
            if self.isMaximized():
                logging.info("Minimizing Window.")
                self.set_btn_icon([self.btn_max], [self.appctxt.get_resource("maximize.png")])
                self.showNormal()
                self.setFixedSize(650, 350)
                self.move(self.rectangle.topLeft())
            else:
                logging.info("Maximizing Window.")
                self.set_btn_icon([self.btn_max], [self.appctxt.get_resource("minimise.png")])
                self.showMaximized()
        else:
            logging.info("Minimizing Window.")
            self.set_btn_icon([self.btn_max], [self.appctxt.get_resource("maximize.png")])
            self.showNormal()

    def mousePressEvent(self, event:QtGui.QMouseEvent):
        """Getting old pos before moving window to new pos."""
        self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event:QtGui.QMouseEvent):
        """Moving window with delta using earlier pos defined by mousePressEvent."""
        self.delta = QtCore.QPoint(event.globalPos() - self.old_pos)
        if not self.isMaximized() == True:
            logging.info("Moving Window...")
            self.move(self.x() + self.delta.x(), self.y() + self.delta.y())
            self.old_pos = event.globalPos()
            if self.old_pos == QtCore.QPoint(self.old_pos.x(), 0):
                self.max()
        elif self.isMaximized() and self.delta.y() > 0:
            self.max()

    def modify_details(self):
        """Opening window allowing to change selected track's tags."""
        logging.info("Opened Modify Details.")
        self.details = ModifyDetails(self.files[self.list.currentRow()], self)
        self.details.show()
        self.stop()

    def next(self):
        logging.info("Playing Next Track.")
        self.nbr = self.list.currentRow() + 1
        if not self.list.count() == self.nbr:
            self.list.setCurrentRow(self.list.currentRow() + 1)
        else:
            self.list.setCurrentRow(0)
            self.nbr = 0
        self.play()

    def open_settings(self):
        """Reading user's settings on disc. Creates setting file if it doesn't exists with default values."""
        logging.info("Reading Settings.")
        if not os.path.exists(os.path.join(cur_dir, "settings.json")):
            logging.info("Creating Settings file.")
            os.makedirs(os.path.join(cur_dir, ""))
            with open(os.path.join(cur_dir, "settings.json"), "w") as a:
                self.settings = {"folder": "C:/Users/pc/Music", "volume": 100, "easter_egg_on": False, "configured": False, "darkmode": False}
                json.dump(self.settings, a)
        with open(os.path.join(cur_dir, "settings.json"), "r") as f:
            self.settings = json.load(f)
            f.close()
        self.sl_volume.setValue(self.settings["volume"])
        if self.settings["easter_egg_on"] == True:
            self.settings["easter_egg_on"] = False
            self.easter_egg()

    def play(self):
        """Plays the selected track."""
        logging.info("Playing Track " + self.files[self.list.currentRow()] + ".")
        self.sound = QtMultimedia.QMediaPlayer()
        self.media = QtCore.QUrl.fromLocalFile(self.files[self.list.currentRow()])
        self.file = QtMultimedia.QMediaContent(self.media)
        self.sound.setMedia(self.file)
        self.set_btn_icon([self.btn_play], [self.appctxt.get_resource("pause.png")])
        self.sound.play()
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.play_bar_n_lb)
        self.timer.start()
        self.refresh_volume()

    def play_bar_n_lb(self):
        """Allowing user to see/edit song's position by showing them on widgets."""
        self.minutes = int(self.sound.duration() / 1000 / 60)
        self.seconds = int(self.sound.duration() / 1000 % 60)
        self.time_bar.setRange(0, self.sound.duration())
        if self.sound.state() == self.sound.state().PlayingState:
            self.time_bar.setValue(self.sound.position())
            self.lb_time.setText(
                f"{int(self.sound.position() / 1000 / 60)}:{int(self.sound.position() / 1000 % 60)} / {self.minutes}:{self.seconds}")
            if self.time_bar.value() == self.sound.duration():
                self.next()

    def play_pause(self):
        if self.sound.state() == self.sound.state().PlayingState:
            logging.info("Pause song.")
            self.sound.pause()
            if self.sound.state() == self.sound.state().PausedState:
                pass
                self.set_btn_icon([self.btn_play], [self.appctxt.get_resource("play.png")])
        elif self.sound.state() == self.sound.state().PausedState:
            logging.info("Play song.")
            self.sound.play()
            if self.sound.state() == self.sound.state().PlayingState:
                pass
                self.set_btn_icon([self.btn_play], [self.appctxt.get_resource("pause.png")])

    def refresh(self):
        logging.info("Refreshing the list.")
        self.list.clear()
        self.get_musics()

    def refresh_volume(self):
        try:
            self.sound.setVolume(self.settings["volume"])
            logging.info("Refreshed the volume.")
        except:
            pass

    def save_settings(self):
        """Writing unsaved settings edits."""
        logging.info("Saving settings.")
        with open(os.path.join(cur_dir, "settings.json"), "w") as c:
            json.dump(self.settings, c)

    @staticmethod
    def set_btn_icon(btn_list, icon_path_list):
        a = 0
        for btn in btn_list:
            btn.setIcon(QtGui.QIcon(icon_path_list[a]))
            a += 1

    @staticmethod
    def set_btn_size(btn_list, H, V):
        for btn in btn_list:
            btn.setFixedSize(H, V)

    @staticmethod
    def set_btn_flat(btn_list, cond):
        for btn in btn_list:
            btn.setFlat(cond)

    def set_folder(self):
        """Asking user the folder where music is located using QFileDialog."""
        logging.info("Opened ''Set folder''.")
        self.ask = QtWidgets.QFileDialog()
        self.ask.setFileMode(self.ask.Directory)
        self.music_dir = self.ask.getExistingDirectory()
        self.settings["folder"] = self.music_dir
        self.save_settings()
        self.refresh()

    def set_time(self):
        logging.info("Setting position in track.")
        self.sound.setPosition(self.time_bar.value())

    def settings_menu(self):
        """Creating the menu of the menu btn."""
        self.setts.addAction(QtGui.QIcon(self.appctxt.get_resource("about.png")), "About", self.about,
                             QtGui.QKeySequence("f10"))
        self.setts.addAction(QtGui.QIcon(self.appctxt.get_resource("help.png")), "Help", self.help,
                             QtGui.QKeySequence("f1"))
        self.setts.addAction(QtGui.QIcon(self.appctxt.get_resource("refresh.png")), "Refresh The List", self.refresh,
                             QtGui.QKeySequence("f5"))
        self.setts.addAction(QtGui.QIcon(self.appctxt.get_resource("folder.png")), "Set The Music Folder",
                             self.set_folder, QtGui.QKeySequence("f2"))

    def set_volume(self):
        logging.info("Setting volume.")
        self.settings["volume"] = self.sl_volume.value()
        self.lb_volume.setText(f"{self.sl_volume.value()}%")
        if self.sl_volume.value() >= 75:
            self.set_sliders_stylesheet("orange", [self.sl_volume])
            self.lb_volume.setStyleSheet("QLabel { color : orange; }")
        elif self.sl_volume.value() < 75:
            self.set_sliders_stylesheet("lightblue", [self.sl_volume])
            self.lb_volume.setStyleSheet("QLabel { color : default; }")
        self.save_settings()
        self.refresh_volume()

    @staticmethod
    def set_sliders_stylesheet(bg_colour, sl_list):
        """Set default style sheet of QSliders.
        :param bg_colour>Any color usable in stylesheet.
        :param sl_list>List of Sliders to be applied to.
        """
        for slider in sl_list:
            slider.setStyleSheet("""QSlider::groove:horizontal {
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
                        background: """ + bg_colour + """;
            }""")

    def show_hide(self):
        """Used by the QSystemTrayIcon."""
        if self.isHidden():
            logging.info("Showing window.")
            self.showNormal()
        else:
            logging.info("Hiding window.")
            self.hide()

    def stop(self):
        """Stops the current playing song."""
        logging.info("Stopping the track.")
        self.sound.stop()
        self.time_bar.setValue(0)
        self.lb_time.setText("0:0 / 0:0")
        self.set_btn_icon([self.btn_play], [self.appctxt.get_resource("play.png")])
        self.timer.stop()
        self.media.clear()
        self.file = QtMultimedia.QMediaContent(self.media)
        self.sound.setMedia(self.file)

    def wizard(self):
        """Opens wizard if first time launch."""
        if not self.settings["configured"]:
            logging.info("Opening Wizard")
            self.dialog = Wizard(cur_dir)
            self.dialog.exec_()
            logging.info("Reading Changes")
            self.open_settings()
        else:
            pass