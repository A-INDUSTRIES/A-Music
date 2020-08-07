"""
Author: DAOUST A. @AINDUSTRIES
Project: A+Music Player
v1.3.0 Pre2
"""
from PySide2 import QtWidgets, QtCore, QtGui

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