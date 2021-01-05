"""
Author: DAOUST A. @AINDUSTRIES
Project: A+Music Player
v2.0.1
"""
from fbs_runtime.application_context.PySide2 import ApplicationContext
from PySide2 import QtWidgets, QtCore, QtGui, QtMultimedia
from glob import glob
from pypresence import Presence

import time, json, os, logging, eyed3, sys, random

LOG_FILE = os.path.join(os.path.join(os.path.expanduser("~"), "A+Music"), "latest_log.txt")
logging.basicConfig(level=logging.INFO, filename=LOG_FILE, filemode="w",
                format='%(asctime)s - %(levelname)s - %(message)s')

cur_dir = os.path.join(os.path.expanduser("~"), "A+Music")
# Gets the folder where setting file is gonna be.

#---------------------------------------------------------------------------------------UI_SECTION---------------------------------------------------------------------------------------

class About(QtWidgets.QMessageBox):

    def __init__(self):
        super().__init__()
        set_style(self)
        self.setWindowTitle("A+Music | About")
        self.setText("""A+Music is a basic music player wich is now playing only mp3.
        This app is open-sourced. Therefore, you can edit the code as you wish.
        This app has been developped by a teenager who is learning.
        If you read this, you're God!
        (Also, click once on the "A" of A+Music...)
        (You can click another time on it to disable the thing.)


        ΔINDUSTRIES.""")

class Error(QtWidgets.QMessageBox):

    def __init__(self, error):
        super().__init__()
        self.setText(error)
        set_style(self)

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
        set_style(self)

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
        self.lb_btn_stop = QtWidgets.QLabel("Click to stop the current playing song.")
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
                           self.btn_setts, ], True)
        if read_settings()["style"] == "normal":
            self.set_btn_icon([self.btn_play,
                               self.btn_next,
                               self.btn_back,
                               self.btn_stop,
                               self.btn_setts],
                              [self.appctxt.get_resource("icons/normal/play.png"),
                               self.appctxt.get_resource("icons/normal/next.png"),
                               self.appctxt.get_resource("icons/normal/back.png"),
                               self.appctxt.get_resource("icons/normal/stop.png"),
                               self.appctxt.get_resource("icons/normal/more.png")])
        else:
            self.set_btn_icon([self.btn_play,
                               self.btn_next,
                               self.btn_back,
                               self.btn_stop,
                               self.btn_setts],
                              [self.appctxt.get_resource("icons/darkmode/play.png"),
                               self.appctxt.get_resource("icons/darkmode/next.png"),
                               self.appctxt.get_resource("icons/darkmode/back.png"),
                               self.appctxt.get_resource("icons/darkmode/stop.png"),
                               self.appctxt.get_resource("icons/darkmode/more.png")])
        self.time_bar.setOrientation(QtCore.Qt.Horizontal)
        self.btn_setts.setMenu(self.setts)
        self.btn_setts.setFixedSize(45, 25)
        self.sl_volume.setPageStep(1)
        self.sl_volume.setOrientation(QtCore.Qt.Horizontal)
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
        if read_settings()["style"] == "normal":
            self.setts.addAction(QtGui.QIcon(self.appctxt.get_resource("icons/normal/about.png")), "About", self.about,
                                 QtGui.QKeySequence("f10"))
            self.setts.addAction(QtGui.QIcon(self.appctxt.get_resource("icons/normal/help.png")), "Help", self.help,
                                 QtGui.QKeySequence("f1"))
            self.setts.addAction(QtGui.QIcon(self.appctxt.get_resource("icons/normal/refresh.png")), "Refresh The List",
                                 self.refresh,
                                 QtGui.QKeySequence("f5"))
            self.setts.addAction(QtGui.QIcon(self.appctxt.get_resource("icons/normal/folder.png")),
                                 "Set The Music Folder",
                                 self.folder, QtGui.QKeySequence("f2"))
            self.setts.addAction(QtGui.QIcon(self.appctxt.get_resource("icons/normal/settings.png")), "Settings",
                                 self.settings, QtGui.QKeySequence("f3"))
        else:
            self.setts.addAction(QtGui.QIcon(self.appctxt.get_resource("icons/darkmode/about.png")), "About",
                                 self.about,
                                 QtGui.QKeySequence("f10"))
            self.setts.addAction(QtGui.QIcon(self.appctxt.get_resource("icons/darkmode/help.png")), "Help", self.help,
                                 QtGui.QKeySequence("f1"))
            self.setts.addAction(QtGui.QIcon(self.appctxt.get_resource("icons/darkmode/refresh.png")),
                                 "Refresh The List",
                                 self.refresh,
                                 QtGui.QKeySequence("f5"))
            self.setts.addAction(QtGui.QIcon(self.appctxt.get_resource("icons/darkmode/folder.png")),
                                 "Set The Music Folder",
                                 self.folder, QtGui.QKeySequence("f2"))
            self.setts.addAction(QtGui.QIcon(self.appctxt.get_resource("icons/darkmode/settings.png")), "Settings",
                                 self.settings, QtGui.QKeySequence("f3"))

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

    def settings(self):
        self.output.setText("Output: Opened settings.")

    def play_mode(self):
        self.output.setText("Output: Change the playing mode.")
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
        self.player = QtMultimedia.QMediaPlayer()
        self.setup_ui()
        set_style(self)
        set_main_ui_icons(self)
        self.rpc_timer = QtCore.QTimer()
        self.rpc_timer.setSingleShot(True)
        self.rpc_timer.setInterval(0)
        self.rpc_timer.timeout.connect(self.set_rpc)
        self.rpc_timer.start()
        self.played_list = []

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
        logging.info("Setting Shortcuts...")
        self.setup_shortcuts()
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
        self.btn_play_mode = QtWidgets.QPushButton()

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
        self.tray_menu.addAction(QtGui.QIcon(self.appctxt.get_resource("icons/normal/play.png")), "Play/Pause", self.play_pause)
        self.tray_menu.addAction(QtGui.QIcon(self.appctxt.get_resource("icons/normal/next.png")), "Next", self.next)
        self.tray_menu.addAction(QtGui.QIcon(self.appctxt.get_resource("icons/normal/back.png")), "Previous", self.back)
        self.tray_menu.addAction(QtGui.QIcon(self.appctxt.get_resource("icons/normal/stop.png")), "Stop", self.stop)
        self.tray_menu.addAction(QtGui.QIcon(self.appctxt.get_resource("icons/normal/close.png")), "Show/Hide", self.show_hide)
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
                           self.btn_stop,
                           self.btn_play_mode], 25, 25)

        self.set_btn_flat([self.btn_close,
                           self.btn_max,
                           self.btn_min,
                           self.btn_play,
                           self.btn_next,
                           self.btn_back,
                           self.btn_stop,
                           self.btn_setts,
                           self.btn_easter_egg,
                           self.btn_play_mode], True)

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

        self.sl_volume.installEventFilter(self)
        self.sl_volume.setMouseTracking(True)
        self.sl_volume.setPageStep(1)
        self.sl_volume.setOrientation(QtCore.Qt.Horizontal)
        self.sl_volume.setRange(0, 100)

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
        self.main_layout.addWidget(self.time_bar, 5, 6, 1, 12)
        self.main_layout.addWidget(self.btn_easter_egg, 1, 1, 2, 1)
        self.main_layout.addWidget(self.btn_play_mode, 5, 5, 1, 1)

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
        self.btn_play_mode.clicked.connect(self.set_play_mode)

    def setup_shortcuts(self):
        self.play_pause_short_a = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_MediaPlay), self)
        self.play_pause_short_a.activated.connect(self.play_pause)

        self.play_pause_short_b = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Space), self)
        self.play_pause_short_b.activated.connect(self.play_pause)

        self.next_short = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_MediaNext), self)
        self.next_short.activated.connect(self.next)

        self.back_short = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_MediaPrevious), self)
        self.back_short.activated.connect(self.back)

        self.stop_short = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_MediaStop), self)
        self.stop_short.activated.connect(self.stop)

        self.volume_up_short = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Up), self)
        self.volume_up_short.activated.connect(self.volume_up)

        self.volume_down_short = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Down), self)
        self.volume_down_short.activated.connect(self.volume_down)

        self.seek_forward_short = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Right), self)
        self.seek_forward_short.activated.connect(self.seek_forward)

        self.seek_backward_short = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Left), self)
        self.seek_backward_short.activated.connect(self.seek_backward)

    #  Methods---------------------------------------------------

    def about(self):
        """Creating About window containing info about the app."""
        logging.info("Opened ''About''")
        self.win = About()
        self.win.exec_()

    def back(self):
        logging.info("Playing last track.")
        try:
            self.played_list.pop(-1)
            self.nbr = self.played_list[-1]
            self.list.setCurrentRow(self.nbr)
            self.played_list.pop(-1)
            self.play()
        except IndexError:
            logging.warning("Played List Index out of range! (No song previously played)")

    def closeEvent(self, event):
        self.RPC.close()
        event.accept()

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
            set_style(self)
            self.lb_title.setStyleSheet("QLabel { color : red; }")
            self.settings["easter_egg_on"] = False
            self.save_settings()
            self.set_volume()
            logging.info("Easter Egg Off.")

    def easter_egg_animate(self):
        """Child of 'easter_egg'. DO NOT USE APPART!
        For each loop, it sets the stylesheet of list, btns, etc to another colour."""
        if self.easter_egg_color_nbr == 0:
            set_main_ui_easter_egg(self, "red")
            set_main_ui_slider(self, "red")
            self.lb_title.setStyleSheet("QLabel { color: red;}")
            self.easter_egg_color_nbr += 1
        elif self.easter_egg_color_nbr == 1:
            set_main_ui_easter_egg(self, "orange")
            set_main_ui_slider(self, "orange")
            self.lb_title.setStyleSheet("QLabel { color: orange;}")
            self.easter_egg_color_nbr += 1
        elif self.easter_egg_color_nbr == 2:
            set_main_ui_easter_egg(self, "yellow")
            set_main_ui_slider(self, "yellow")
            self.lb_title.setStyleSheet("QLabel { color: yellow;}")
            self.easter_egg_color_nbr += 1
        elif self.easter_egg_color_nbr == 3:
            set_main_ui_easter_egg(self, "green")
            set_main_ui_slider(self, "green")
            self.lb_title.setStyleSheet("QLabel { color: green;}")
            self.easter_egg_color_nbr += 1
        elif self.easter_egg_color_nbr == 4:
            set_main_ui_easter_egg(self, "blue")
            set_main_ui_slider(self, "blue")
            self.lb_title.setStyleSheet("QLabel { color: red;}")
            self.easter_egg_color_nbr += 1
        elif self.easter_egg_color_nbr == 5:
            set_main_ui_easter_egg(self, "purple")
            set_main_ui_slider(self, "purple")
            self.lb_title.setStyleSheet("QLabel { color: purple;}")
            self.easter_egg_color_nbr += 1
        elif self.easter_egg_color_nbr == 6:
            set_main_ui_easter_egg(self, "pink")
            set_main_ui_slider(self, "pink")
            self.lb_title.setStyleSheet("QLabel { color: pink;}")
            self.easter_egg_color_nbr += 1
        elif self.easter_egg_color_nbr == 7:
            set_main_ui_easter_egg(self, "brown")
            set_main_ui_slider(self, "brown")
            self.lb_title.setStyleSheet("QLabel { color: brown;}")
            self.easter_egg_color_nbr += 1
        elif self.easter_egg_color_nbr == 8:
            set_main_ui_easter_egg(self, "white")
            set_main_ui_slider(self, "white")
            self.lb_title.setStyleSheet("QLabel { color: white;}")
            self.easter_egg_color_nbr += 1
        elif self.easter_egg_color_nbr == 9:
            set_main_ui_easter_egg(self, "gray")
            set_main_ui_slider(self, "gray")
            self.lb_title.setStyleSheet("QLabel { color: gray;}")
            self.easter_egg_color_nbr += 1
        elif self.easter_egg_color_nbr == 10:
            set_main_ui_easter_egg(self, "black")
            set_main_ui_slider(self, "black")
            self.lb_title.setStyleSheet("QLabel { color: black;}")
            self.easter_egg_color_nbr = 0

    def eventFilter(self, watched: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """Showing volume bar if label hovered. Hiding if unhovered."""
        if watched == self.lb_img_volume and event.type() == QtCore.QEvent.Enter:
            logging.info("Showing Volume Bar...")
            self.show_volume()
        elif watched == self.sl_volume and event.type() == QtCore.QEvent.Leave:
            logging.info("Hiding Volume Bar...")
            self.hide_volume()
        return super().eventFilter(watched, event)

    def get_musics(self):
        """Searching user defined folder to find all .mp3 files and adding them to the list."""
        logging.info("Getting Musics.")
        self.list.addItems(list_musics())
        self.nbr = 0

    def help(self):
        """Obviously... It opens help."""
        logging.info("Opened Help.")
        self.help_win = Help(self.appctxt)
        self.help_win.show()

    def hide_volume(self):
        self.main_layout.removeWidget(self.lb_volume)
        self.main_layout.removeWidget(self.sl_volume)
        self.main_layout.removeWidget(self.lb_img_volume)
        self.main_layout.removeWidget(self.time_bar)
        self.main_layout.addWidget(self.lb_img_volume, 5, 18, 1, 1)
        self.main_layout.addWidget(self.time_bar, 5, 6, 1, 12)
        self.sl_volume.setHidden(True)
        self.lb_volume.setHidden(True)

    def max(self):
        """Maximizing or minimizing window based on current state."""
        if not self.isFullScreen():
            if self.isMaximized():
                logging.info("Minimizing Window.")
                if self.settings["style"] == "normal":
                    self.set_btn_icon([self.btn_max], [self.appctxt.get_resource("icons/normal/maximize.png")])
                else:
                    self.set_btn_icon([self.btn_max], [self.appctxt.get_resource("icons/darkmode/maximize.png")])
                self.showNormal()
                self.setFixedSize(650, 350)
                self.move(self.rectangle.topLeft())
            else:
                logging.info("Maximizing Window.")
                if self.settings["style"] == "normal":
                    self.set_btn_icon([self.btn_max], [self.appctxt.get_resource("icons/normal/minimise.png")])
                else:
                    self.set_btn_icon([self.btn_max], [self.appctxt.get_resource("icons/darkmode/minimise.png")])
                self.showMaximized()
        else:
            logging.info("Minimizing Window.")
            if self.settings["style"] == "normal":
                self.set_btn_icon([self.btn_max], [self.appctxt.get_resource("icons/normal/maximize.png")])
            else:
                self.set_btn_icon([self.btn_max], [self.appctxt.get_resource("icons/darkmode/maximize.png")])
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
        self.details = ModifyDetails(list_files()[self.list.currentRow()], self)
        self.details.show()
        self.stop()

    def next(self):
        logging.info("Playing Next Track.")
        if not self.settings["play_mode"] == "shuffle":
            self.nbr = self.list.currentRow() + 1
            if not self.list.count() == self.nbr:
                self.list.setCurrentRow(self.list.currentRow() + 1)
            else:
                self.list.setCurrentRow(0)
                self.nbr = 0
        else:
            self.list.setCurrentRow(random.randint(0, self.list.count()))
        self.play()

    def open_settings(self):
        """Reading user's settings on disc. Creates setting file if it doesn't exists with default values."""
        logging.info("Reading Settings.")
        self.settings = read_settings()
        self.sl_volume.setValue(self.settings["volume"])
        if self.settings["easter_egg_on"] == True:
            self.settings["easter_egg_on"] = False
            self.easter_egg()

    def play(self):
        """Plays the selected track."""
        logging.info("Playing Track " + list_files()[self.list.currentRow()] + ".")
        self.media = QtCore.QUrl.fromLocalFile(list_files()[self.list.currentRow()])
        self.file = QtMultimedia.QMediaContent(self.media)
        self.player.setMedia(self.file)
        self.played_list.append(self.list.currentRow())
        if self.settings["style"] == "normal":
            self.set_btn_icon([self.btn_play], [self.appctxt.get_resource("icons/normal/pause.png")])
        else:
            self.set_btn_icon([self.btn_play], [self.appctxt.get_resource("icons/darkmode/pause.png")])
        self.player.play()
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.play_bar_n_lb)
        self.timerb = QtCore.QTimer()
        self.timerb.setInterval(500)
        self.timerb.setSingleShot(True)
        self.timerb.timeout.connect(self.update_rpc)
        self.timer.start()
        self.timerb.start()
        self.refresh_volume()

    def play_bar_n_lb(self):
        """Allowing user to see/edit song's position by showing them on widgets."""
        self.minutes = int(self.player.duration() / 1000 / 60)
        self.seconds = int(self.player.duration() / 1000 % 60)
        self.time_bar.setRange(0, self.player.duration())
        if self.player.state() == QtMultimedia.QMediaPlayer.PlayingState:
            self.time_bar.setValue(self.player.position())
            self.lb_time.setText(
                f"{int(self.player.position() / 1000 / 60)}:{int(self.player.position() / 1000 % 60)} / {self.minutes}:{self.seconds}")
        elif self.player.mediaStatus() == QtMultimedia.QMediaPlayer.MediaStatus.EndOfMedia:
            self.next()

    def play_pause(self):
        if self.player.state() == self.player.state().PlayingState:
            logging.info("Pause song.")
            self.player.pause()
            if self.player.state() == self.player.state().PausedState:
                if self.settings["style"] == "normal":
                    self.set_btn_icon([self.btn_play], [self.appctxt.get_resource("icons/normal/play.png")])
                else:
                    self.set_btn_icon([self.btn_play], [self.appctxt.get_resource("icons/darkmode/play.png")])
        elif self.player.state() == self.player.state().PausedState:
            logging.info("Play song.")
            self.player.play()
            if self.player.state() == self.player.state().PlayingState:
                if self.settings["style"] == "normal":
                    self.set_btn_icon([self.btn_play], [self.appctxt.get_resource("icons/normal/pause.png")])
                else:
                    self.set_btn_icon([self.btn_play], [self.appctxt.get_resource("icons/darkmode/pause.png")])

    def refresh(self):
        logging.info("Refreshing the list.")
        self.list.clear()
        self.get_musics()

    def refresh_volume(self):
        try:
            self.player.setVolume(self.settings["volume"])
            logging.info("Refreshed the volume.")
        except:
            pass

    def save_settings(self):
        """Writing unsaved settings edits."""
        logging.info("Saving settings.")
        write_settings(self.settings)

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

    def set_play_mode(self):
        if self.settings["play_mode"] == "straight":
            self.settings["play_mode"] = "shuffle"
            write_settings(self.settings)
        elif self.settings["play_mode"] == "shuffle":
            self.settings["play_mode"] = "straight"
            write_settings(self.settings)
        set_main_ui_icons(self)

    def set_time(self):
        logging.info("Setting position in track.")
        self.player.setPosition(self.time_bar.value())

    def settings_menu(self):
        """Creating the menu of the menu btn."""
        if self.settings["style"] == "normal":
            self.setts.addAction(QtGui.QIcon(self.appctxt.get_resource("icons/normal/about.png")), "About", self.about,
                                 QtGui.QKeySequence("f10"))
            self.setts.addAction(QtGui.QIcon(self.appctxt.get_resource("icons/normal/help.png")), "Help", self.help,
                                 QtGui.QKeySequence("f1"))
            self.setts.addAction(QtGui.QIcon(self.appctxt.get_resource("icons/normal/refresh.png")), "Refresh The List", self.refresh,
                                 QtGui.QKeySequence("f5"))
            self.setts.addAction(QtGui.QIcon(self.appctxt.get_resource("icons/normal/folder.png")), "Set The Music Folder",
                                 self.set_folder, QtGui.QKeySequence("f2"))
            self.setts.addAction(QtGui.QIcon(self.appctxt.get_resource("icons/normal/settings.png")), "Settings",
                                 self.set_settings, QtGui.QKeySequence("f3"))
        else:
            self.setts.addAction(QtGui.QIcon(self.appctxt.get_resource("icons/darkmode/about.png")), "About", self.about,
                                 QtGui.QKeySequence("f10"))
            self.setts.addAction(QtGui.QIcon(self.appctxt.get_resource("icons/darkmode/help.png")), "Help", self.help,
                                 QtGui.QKeySequence("f1"))
            self.setts.addAction(QtGui.QIcon(self.appctxt.get_resource("icons/darkmode/refresh.png")), "Refresh The List",
                                 self.refresh,
                                 QtGui.QKeySequence("f5"))
            self.setts.addAction(QtGui.QIcon(self.appctxt.get_resource("icons/darkmode/folder.png")),
                                 "Set The Music Folder",
                                 self.set_folder, QtGui.QKeySequence("f2"))
            self.setts.addAction(QtGui.QIcon(self.appctxt.get_resource("icons/darkmode/settings.png")), "Settings",
                                 self.set_settings, QtGui.QKeySequence("f3"))

    def set_rpc(self):
        self.client_id = "783388836049977396"
        self.RPC = Presence(client_id=self.client_id)
        self.RPC.connect()
        self.time_stamp = time.time()
        self.RPC.update(large_image="a-music-ico", state=f"Listening to A+Music", start=self.time_stamp)

    def update_rpc(self):
        self._song = read_music_attributes(list_files()[self.list.currentRow()])
        self.time_stamp = time.time()
        self.max_time = time.time() + self.player.duration()/1000
        if not self._song["title"] == None and not self._song["artist"] == None:
            self.RPC.update(large_image="a-music-ico", details=f"Listening to " + self._song["title"], start=self.time_stamp, state=f"from " + self._song["artist"], end=self.max_time)
        elif self._song["title"] == None and not self._song["artist"] == None:
            self.RPC.update(large_image="a-music-ico", details=f"Listening to Unknown", start=self.time_stamp, state=f"from " + self._song["artist"], end=self.max_time)
        elif self._song["artist"] == None and not self._song["title"] == None:
            self.RPC.update(large_image="a-music-ico", details=f"Listening to " + self._song["title"], start=self.time_stamp, state=f"from Unknown", end=self.max_time)
        else:
            self.RPC.update(large_image="a-music-ico", details=f"Listening to Unknown", start=self.time_stamp, state=f"from Unknown", end=self.max_time)

    def set_volume(self):
        logging.info("Setting volume.")
        self.settings["volume"] = self.sl_volume.value()
        self.lb_volume.setText(f"{self.sl_volume.value()}%")
        if self.sl_volume.value() >= 75:
            set_main_ui_slider(self, "orange")
        elif self.sl_volume.value() < 75:
            set_main_ui_slider(self, "default")
        self.save_settings()
        self.refresh_volume()

    def set_settings(self):
        self.win = Settings(self)
        self.win.show()

    def seek_forward(self):
        self.time_bar.setValue(self.time_bar.value()+5000)
        self.set_time()

    def seek_backward(self):
        self.time_bar.setValue(self.time_bar.value()-5000)
        self.set_time()

    def show_hide(self):
        """Used by the QSystemTrayIcon."""
        if self.isHidden():
            logging.info("Showing window.")
            self.showNormal()
        else:
            logging.info("Hiding window.")
            self.hide()

    def show_volume(self):
        self.main_layout.removeWidget(self.lb_img_volume)
        self.main_layout.removeWidget(self.time_bar)
        self.main_layout.addWidget(self.lb_volume, 5, 18, 1, 1)
        self.main_layout.addWidget(self.sl_volume, 5, 16, 1, 2)
        self.main_layout.addWidget(self.lb_img_volume, 5, 15, 1, 1)
        self.main_layout.addWidget(self.time_bar, 5, 6, 1, 9)
        self.sl_volume.setHidden(False)
        self.lb_volume.setHidden(False)

    def stop(self):
        """Stops the current playing song."""
        logging.info("Stopping the track.")
        self.player.stop()
        self.time_bar.setValue(0)
        self.lb_time.setText("0:0 / 0:0")
        if self.settings["style"] == "normal":
            self.set_btn_icon([self.btn_play], [self.appctxt.get_resource("icons/normal/play.png")])
        else:
            self.set_btn_icon([self.btn_play], [self.appctxt.get_resource("icons/darkmode/play.png")])
        self.timer.stop()
        self.media.clear()
        self.file = QtMultimedia.QMediaContent(self.media)
        self.player.setMedia(self.file)

    def volume_up(self):
        self.show_volume()
        self.sl_volume.setValue(self.sl_volume.value()+2)
        self.volume_timer = QtCore.QTimer()
        self.volume_timer.setSingleShot(True)
        self.volume_timer.setInterval(2000)
        self.volume_timer.timeout.connect(self.hide_volume)
        self.volume_timer.start()

    def volume_down(self):
        self.show_volume()
        self.sl_volume.setValue(self.sl_volume.value()-2)
        self.volume_timer = QtCore.QTimer()
        self.volume_timer.setSingleShot(True)
        self.volume_timer.setInterval(2000)
        self.volume_timer.timeout.connect(self.hide_volume)
        self.volume_timer.start()

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

class ModifyDetails(QtWidgets.QWidget):

    def __init__(self, file, mainwindow):
        super().__init__()
        self.file = file
        self.mainwindow = mainwindow
        self.setup_ui()
        set_style(self)

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
        self.le_title.setText(read_music_attributes(self.file)["title"])
        self.le_artist.setText(read_music_attributes(self.file)["artist"])

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
        write_music_attributes(self.file, self.le_title.text(), self.le_artist.text())
        self.close()
        self.mainwindow.refresh()

class Settings(QtWidgets.QWidget):

    def __init__(self, main_window):
        super().__init__()
        self.settings = read_settings()
        self.main_window = main_window
        self.setup_ui()
        set_style(self)

    def setup_ui(self):
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layout()
        self.setup_connections()

    def create_widgets(self):
        self.label = QtWidgets.QLabel("Playback speed:")
        self.bar = QtWidgets.QSlider()
        self.speed = QtWidgets.QLabel()
        self.style_lb = QtWidgets.QLabel("Style:")
        self.style_cb = QtWidgets.QComboBox()
        self.btn = QtWidgets.QPushButton("Ok")

    def modify_widgets(self):
        self.bar.setRange(50, 150)
        self.bar.setValue(100)
        self.bar.setOrientation(QtCore.Qt.Horizontal)
        self.bar.setSingleStep(1)
        self.bar.setPageStep(1)
        if self.main_window.player.playbackRate() == 0.0:
            self.bar.setValue(100)
        else:
            self.bar.setValue(int(self.main_window.player.playbackRate()*100))
        self.set_speed()
        self.style_cb.addItems(["Normal", "Dark"])
        if self.settings["style"] == "normal":
            self.style_cb.setCurrentIndex(0)
        else:
            self.style_cb.setCurrentIndex(1)

    def create_layouts(self):
        self.layout = QtWidgets.QVBoxLayout(self)

    def add_widgets_to_layout(self):
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.bar)
        self.layout.addWidget(self.speed)
        self.layout.addWidget(self.style_lb)
        self.layout.addWidget(self.style_cb)
        self.layout.addWidget(self.btn)

    def setup_connections(self):
        self.btn.clicked.connect(self.close)
        self.bar.valueChanged.connect(self.set_speed)
        self.style_cb.activated.connect(self.set_style)

    def set_speed(self):
        self.main_window.player.setPlaybackRate(self.bar.value()/100)
        if self.bar.value() == 50:
            self.speed.setText("Speed: 1/4x")
        elif self.bar.value() == 75:
            self.speed.setText("Speed: 1/2x")
        elif self.bar.value() == 100:
            self.speed.setText("Speed: 1x")
        elif self.bar.value() == 125:
            self.speed.setText("Speed: 2x")
        elif self.bar.value() == 150:
            self.speed.setText("Speed: 4x")
        else:
            self.speed.setText("Speed: " + str(self.bar.value()))

    def set_style(self):
        self.settings["style"] = self.style_cb.currentText().lower()
        write_settings(self.settings)
        set_style(self)
        set_style(self.main_window)
        set_main_ui_icons(self.main_window)
        self.settings = read_settings()

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
        self.page1_ = QtWidgets.QWizardPage()
        self.page1_.setTitle("Quick Setup")
        self.page1_.setSubTitle("This is the First Time setup.\nIt will help you configure the app.")

    def page2(self):
        self.page2_ = QtWidgets.QWizardPage()
        self.page2_.setTitle("Quick Setup")
        self.page2_.setSubTitle("Set default values.")
        self.page2_btn = QtWidgets.QPushButton("Open Directory")
        self.page2_lb = QtWidgets.QLabel("C:/Users/pc/Music")
        self.page2_lb_vol = QtWidgets.QLabel("Volume:")
        self.page2_lb_vol_perc = QtWidgets.QLabel("100%")
        self.page2_sl = QtWidgets.QSlider()
        self.page2_style_lb = QtWidgets.QLabel("Style:")
        self.page2_style_cb = QtWidgets.QComboBox()
        self.page2_style_cb.addItems(["Normal", "Dark"])
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
        self.page2_layout = QtWidgets.QGridLayout(self.page2_)
        self.page2_layout.addWidget(self.page2_btn, 1, 4)
        self.page2_layout.addWidget(self.page2_lb, 1, 1, 1, 3)
        self.page2_layout.addWidget(self.page2_sl, 2, 3)
        self.page2_layout.addWidget(self.page2_lb_vol, 2, 1)
        self.page2_layout.addWidget(self.page2_lb_vol_perc, 2, 4)
        self.page2_layout.addWidget(self.page2_style_lb, 3, 1)
        self.page2_layout.addWidget(self.page2_style_cb, 3, 4)
        self.page2_btn.clicked.connect(self.page2_set_folder)
        self.page2_sl.valueChanged.connect(self.page2_set_volume)
        self.page2_style_cb.activated.connect(self.page2_set_style)

    def page3(self):
        self.page3_ = QtWidgets.QWizardPage()
        self.page3_.setTitle("Quick Setup")
        self.page3_.setSubTitle("Done!\nThe app is now ready to go!")

    def add_pages(self):
        self.addPage(self.page1_)
        self.addPage(self.page2_)
        self.addPage(self.page3_)

    #   Methods---------------------------------------------------

    def open_settings(self):
        self.settings = read_settings()
        self.settings["folder"] = "C:/Users/pc/Music"
        self.settings["volume"] = 100
        self.settings["easter_egg_on"] = False

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

    def page2_set_style(self):
        self.settings["style"] = self.page2_style_cb.currentText().lower()
        self.save_settings()

    def save_settings(self):
        self.settings["configured"] = True
        write_settings(self.settings)

#-------------------------------------------------------------------------------------UI_SECTION_END-------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------API_SECTION--------------------------------------------------------------------------------------

def list_files():
    return glob(os.path.join(read_settings()["folder"], "*.mp3"))

def list_musics():
    filelist = []
    for file in list_files():
        if not read_music_attributes(file)["title"] == "None" and \
                not read_music_attributes(file)["artist"] == "None":
            filelist.append(read_music_attributes(file)["title"] + " | " +
                            read_music_attributes(file)["artist"])
        else:
            filelist.append(read_music_attributes(file)["title"] + " | " +
                            read_music_attributes(file)["artist"] + " ~" +
                            os.path.basename(file))
    return filelist

def read_music_attributes(file):
    try:
        tag = eyed3.load(file).tag
    except:
        return {"title": "None", "artist": "None"}
    return {"title": str(tag.title), "artist": str(tag.artist)}

def write_music_attributes(file, title, artist):
    tag = eyed3.load(file).tag
    tag.title = title
    tag.artist = artist
    try:
        tag.save()
    except PermissionError:
        error = Error("PermissionError : Can't write tag to file.\nPlease check file premissions.")
        error.exec_()

def create_settings():
    os.makedirs(os.path.join(cur_dir, ""), exist_ok=True)
    with open(os.path.join(cur_dir, "settings.json"), "w") as a:
        settings = {"folder": "C:/Users/pc/Music", "volume": 100, "easter_egg_on": False, "configured": False,
                    "style": "normal", "play_mode": "straight"}
        json.dump(settings, a)

def read_settings():
    if not os.path.exists(os.path.join(cur_dir, "settings.json")):
        create_settings()
    with open(os.path.join(cur_dir, "settings.json"), "r") as f:
        settings = json.load(f)
        try:
            if settings["style"] and settings["play_mode"]:
                return settings
        except KeyError:
            create_settings()
            with open(os.path.join(cur_dir, "settings.json"), "r") as f:
                return json.load(f)

def write_settings(settings) -> list:
    with open(os.path.join(cur_dir, "settings.json"), "w") as c:
        json.dump(settings, c)

def set_style(self):
    if read_settings()["style"] == "dark":
        self.setStyleSheet("""QWidget {
    background: rgb(40,43,48);
}

QLabel {
color: rgb(114,137,218);
}

QSlider::groove:horizontal {
    border: 1px;
    height: 10px;
    background: rgb(54,57,62);
}

QSlider::handle:horizontal {
    background: red;
    border: 1px;
    width: 5px;
    margin: -5px 0;
    border-radius: 2px;
}

QSlider::sub-page:horizontal {
    background: rgb(114,137,218);
}

QListWidget {
    color: rgb(114,137,218);
    alternate-background-color: rgb(54,57,62);
}

QMenu {
    background-color: rgb(40,43,48);
    border: 1px solid black;
}

QMenu::item {
    background-color: transparent;
}

QMenu::item:selected {
    background-color: rgb(114,137,218);
}

QPushButton {
    background-color: rgb(54,57,62);
    color: rgb(114,137,218);
}

QComboBox {
    color: rgb(114,137,218);
}

QLineEdit {
    color: rgb(114,137,218);
}
""")
    else:
        self.setStyleSheet("""
QSlider::groove:horizontal {
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
}
""")

def set_main_ui_icons(self):
    if read_settings()["style"] == "normal":
        self.set_btn_icon([self.btn_close,
                               self.btn_max,
                               self.btn_min,
                               self.btn_play,
                               self.btn_next,
                               self.btn_back,
                               self.btn_stop,
                               self.btn_setts],
                              [self.appctxt.get_resource("icons/normal/close.png"),
                               self.appctxt.get_resource("icons/normal/maximize.png"),
                               self.appctxt.get_resource("icons/normal/min.png"),
                               self.appctxt.get_resource("icons/normal/play.png"),
                               self.appctxt.get_resource("icons/normal/next.png"),
                               self.appctxt.get_resource("icons/normal/back.png"),
                               self.appctxt.get_resource("icons/normal/stop.png"),
                               self.appctxt.get_resource("icons/normal/more.png")])
        self.pix = QtGui.QPixmap(self.appctxt.get_resource("icons/normal/volume.png"))
        self.lb_img_volume.setPixmap(self.pix.scaled(25, 25))
        if read_settings()["play_mode"] == "straight":
            self.set_btn_icon([self.btn_play_mode],[self.appctxt.get_resource("icons/normal/right-arrow.png")])
        else:
            self.set_btn_icon([self.btn_play_mode],[self.appctxt.get_resource("icons/normal/shuffle.png")])
        if self.player.state() == self.player.state().PlayingState:
            self.set_btn_icon([self.btn_play], [self.appctxt.get_resource("icons/normal/pause.png")])
        else:
            self.set_btn_icon([self.btn_play], [self.appctxt.get_resource("icons/normal/play.png")])
    else:
        self.set_btn_icon([self.btn_close,
                                   self.btn_max,
                                   self.btn_min,
                                   self.btn_play,
                                   self.btn_next,
                                   self.btn_back,
                                   self.btn_stop,
                                   self.btn_setts,],
                                  [self.appctxt.get_resource("icons/darkmode/close.png"),
                                   self.appctxt.get_resource("icons/darkmode/maximize.png"),
                                   self.appctxt.get_resource("icons/darkmode/min.png"),
                                   self.appctxt.get_resource("icons/darkmode/play.png"),
                                   self.appctxt.get_resource("icons/darkmode/next.png"),
                                   self.appctxt.get_resource("icons/darkmode/back.png"),
                                   self.appctxt.get_resource("icons/darkmode/stop.png"),
                                   self.appctxt.get_resource("icons/darkmode/more.png")])
        self.pix = QtGui.QPixmap(self.appctxt.get_resource("icons/darkmode/volume.png"))
        self.lb_img_volume.setPixmap(self.pix.scaled(25, 25))
        if read_settings()["play_mode"] == "straight":
            self.set_btn_icon([self.btn_play_mode],[self.appctxt.get_resource("icons/darkmode/right-arrow.png")])
        else:
            self.set_btn_icon([self.btn_play_mode],[self.appctxt.get_resource("icons/darkmode/shuffle.png")])
        if self.player.state() == self.player.state().PlayingState:
            self.set_btn_icon([self.btn_play], [self.appctxt.get_resource("icons/darkmode/pause.png")])
        else:
            self.set_btn_icon([self.btn_play], [self.appctxt.get_resource("icons/darkmode/play.png")])

def set_main_ui_easter_egg(self, color) -> str:
    if read_settings()["style"] == "normal":
        self.setStyleSheet("""
QSlider::groove:horizontal {
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
    background: """ + color + """;
}

QLabel { color: """ + color + """;}

QListWidget::item { color: """ + color + """;}""")
    else:
        self.setStyleSheet("""QWidget {
    background: rgb(40,43,48);
}

QLabel {
color: """ + color + """;
}

QSlider::groove:horizontal {
    border: 1px;
    height: 10px;
    background: rgb(54,57,62);
}

QSlider::handle:horizontal {
    background: red;
    border: 1px;
    width: 5px;
    margin: -5px 0;
    border-radius: 2px;
}

QSlider::sub-page:horizontal {
    background: """ + color + """;
}

QListWidget {
    color: rgb(114,137,218);
    alternate-background-color: rgb(54,57,62);
}

QListWidget::item { color: """ + color + """;}

QMenu {
    background-color: rgb(40,43,48);
    border: 1px solid black;
}

QMenu::item {
    background-color: transparent;
}

QMenu::item:selected {
    background-color: rgb(114,137,218);
}

QPushButton {
    background-color: rgb(54,57,62);
    color: rgb(114,137,218);
}

QComboBox {
    color: rgb(114,137,218);
}
""")
def set_main_ui_slider(self, color):
    if read_settings()["style"] == "normal":
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
                        background: """ + color + """;
            }""")
    else:
        self.sl_volume.setStyleSheet("""QSlider::groove:horizontal {
                                    border: 1px;
                                    height: 10px;
                                    background: rgb(54,57,62);
                                }

                                QSlider::handle:horizontal {
                                    background: red;
                                    border: 1px;
                                    width: 5px;
                                    margin: -5px 0;
                                    border-radius: 2px;
                                }

                                QSlider::sub-page:horizontal {
                                    background: """ + color + """;
                        }""")
    self.lb_volume.setStyleSheet("QLabel { color: " + color + ";}")
    if color == "default":
        if read_settings()["style"] == "normal":
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
            self.lb_volume.setStyleSheet("QLabel { color: black;}")
        else:
            self.sl_volume.setStyleSheet("""QSlider::groove:horizontal {
                                            border: 1px;
                                            height: 10px;
                                            background: rgb(54,57,62);
                                        }

                                        QSlider::handle:horizontal {
                                            background: red;
                                            border: 1px;
                                            width: 5px;
                                            margin: -5px 0;
                                            border-radius: 2px;
                                        }

                                        QSlider::sub-page:horizontal {
                                            background: rgb(114,137,218);
                                }""")
            self.lb_volume.setStyleSheet("QLabel { color: rgb(114,137,218);}")

#------------------------------------------------------------------------------------API_SECTION_END------------------------------------------------------------------------------------


if __name__ == '__main__':
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    window = MainWindow(appctxt)
    window.showNormal()
    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)