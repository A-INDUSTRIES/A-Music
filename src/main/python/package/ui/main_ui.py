"""
Author: DAOUST A. @AINDUSTRIES
Project: A+Music Player
v1.4.0Pre2
"""
from PySide2 import QtWidgets, QtCore, QtGui, QtMultimedia
from glob import glob
from pypresence import Presence

from package.ui.help_ui import Help
from package.ui.details_ui import ModifyDetails
from package.ui.wizard_ui import Wizard
from package.ui.settings_ui import Settings
from package.ui.about_ui import About

from package.api.player_api import *
from package.api.settings_api import *
from package.api.logging_api import *
from package.api.style_api import *

import time

class MainWindow(QtWidgets.QWidget):

    def __init__(self, appctxt):
        super().__init__()
        self.appctxt = appctxt
        log_info("Initialized Logging.")
        self.resize(650, 350)
        log_info("Resizing MainWindow.")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        log_info("Set MainWindow Frameless.")
        self.rectangle = self.frameGeometry()
        self.centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        self.rectangle.moveCenter(self.centerPoint)
        self.move(self.rectangle.topLeft())
        log_info("Moved window to center of screen.")
        log_info("Setting up the ui.")
        self.player = QtMultimedia.QMediaPlayer()
        self.style_ = Style(self)
        self.setup_ui()
        self.style_.set_style()
        self.style_.set_main_ui_icons()
        self.rpc_timer = QtCore.QTimer()
        self.rpc_timer.setSingleShot(True)
        self.rpc_timer.setInterval(0)
        self.rpc_timer.timeout.connect(self.set_rpc)
        self.rpc_timer.start()

    def setup_ui(self):
        log_info("Creating Widgets...")
        self.create_widgets()
        log_info("Creating System Tray...")
        self.create_sys_tray_icon()
        log_info("Modifying Widgets...")
        self.modify_widgets()
        log_info("Creating Layout...")
        self.create_layouts()
        log_info("Adding Widgets to Layout...")
        self.add_widgets_to_layouts()
        log_info("Setting Connections...")
        self.setup_connections()
        log_info("Setting Shortcuts...")
        self.setup_shortcuts()
        log_info("Opening Settings.")
        self.open_settings()
        log_info("Setting the Menu.")
        self.settings_menu()
        log_info("Making Wizard if First Time.")
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
        log_info("Opened ''About''")
        self.win = About()
        self.win.exec_()

    def back(self):
        log_info("Playing last track.")
        self.nbr = self.list.currentRow() - 1
        if not self.nbr == -1:
            self.list.setCurrentRow(self.list.currentRow() - 1)
        else:
            self.list.setCurrentRow(self.list.count() - 1)
            self.nbr = self.list.count() - 1
        self.play()

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
            log_info("Easter Egg Activated!")
        elif self.settings["easter_egg_on"] == True:
            self.easter_egg_timer.stop()
            self.style_.set_style()
            self.lb_title.setStyleSheet("QLabel { color : red; }")
            self.settings["easter_egg_on"] = False
            self.save_settings()
            log_info("Easter Egg Off.")

    def easter_egg_animate(self):
        """Child of 'easter_egg'. DO NOT USE APPART!
        For each loop, it sets the stylesheet of list, btns, etc to another colour."""
        if self.easter_egg_color_nbr == 0:
            self.style_.set_main_ui_easter_egg("red")
            self.style_.set_main_ui_slider("red")
            self.lb_title.setStyleSheet("QLabel { color: red;}")
            self.easter_egg_color_nbr += 1
        elif self.easter_egg_color_nbr == 1:
            self.style_.set_main_ui_easter_egg("orange")
            self.style_.set_main_ui_slider("orange")
            self.lb_title.setStyleSheet("QLabel { color: orange;}")
            self.easter_egg_color_nbr += 1
        elif self.easter_egg_color_nbr == 2:
            self.style_.set_main_ui_easter_egg("yellow")
            self.style_.set_main_ui_slider("yellow")
            self.lb_title.setStyleSheet("QLabel { color: yellow;}")
            self.easter_egg_color_nbr += 1
        elif self.easter_egg_color_nbr == 3:
            self.style_.set_main_ui_easter_egg("green")
            self.style_.set_main_ui_slider("green")
            self.lb_title.setStyleSheet("QLabel { color: green;}")
            self.easter_egg_color_nbr += 1
        elif self.easter_egg_color_nbr == 4:
            self.style_.set_main_ui_easter_egg("blue")
            self.style_.set_main_ui_slider("blue")
            self.lb_title.setStyleSheet("QLabel { color: red;}")
            self.easter_egg_color_nbr += 1
        elif self.easter_egg_color_nbr == 5:
            self.style_.set_main_ui_easter_egg("purple")
            self.style_.set_main_ui_slider("purple")
            self.lb_title.setStyleSheet("QLabel { color: purple;}")
            self.easter_egg_color_nbr += 1
        elif self.easter_egg_color_nbr == 6:
            self.style_.set_main_ui_easter_egg("pink")
            self.style_.set_main_ui_slider("pink")
            self.lb_title.setStyleSheet("QLabel { color: pink;}")
            self.easter_egg_color_nbr += 1
        elif self.easter_egg_color_nbr == 7:
            self.style_.set_main_ui_easter_egg("brown")
            self.style_.set_main_ui_slider("brown")
            self.lb_title.setStyleSheet("QLabel { color: brown;}")
            self.easter_egg_color_nbr += 1
        elif self.easter_egg_color_nbr == 8:
            self.style_.set_main_ui_easter_egg("white")
            self.style_.set_main_ui_slider("white")
            self.lb_title.setStyleSheet("QLabel { color: white;}")
            self.easter_egg_color_nbr += 1
        elif self.easter_egg_color_nbr == 9:
            self.style_.set_main_ui_easter_egg("gray")
            self.style_.set_main_ui_slider("gray")
            self.lb_title.setStyleSheet("QLabel { color: gray;}")
            self.easter_egg_color_nbr += 1
        elif self.easter_egg_color_nbr == 10:
            self.style_.set_main_ui_easter_egg("black")
            self.style_.set_main_ui_slider("black")
            self.lb_title.setStyleSheet("QLabel { color: black;}")
            self.easter_egg_color_nbr = 0

    def eventFilter(self, watched: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """Showing volume bar if label hovered. Hiding if unhovered."""
        if watched == self.lb_img_volume and event.type() == QtCore.QEvent.Enter:
            log_info("Showing Volume Bar...")
            self.show_volume()
        elif watched == self.sl_volume and event.type() == QtCore.QEvent.Leave:
            log_info("Hiding Volume Bar...")
            self.hide_volume()
        return super().eventFilter(watched, event)

    def get_musics(self):
        """Searching user defined folder to find all .mp3 files and adding them to the list."""
        log_info("Getting Musics.")
        self.list.addItems(list_musics())
        self.nbr = 0

    def help(self):
        """Obviously... It opens help."""
        log_info("Opened Help.")
        self.help_win = Help(self.appctxt)
        self.help_win.show()

    def hide_volume(self):
        self.main_layout.removeWidget(self.lb_volume)
        self.main_layout.removeWidget(self.sl_volume)
        self.main_layout.removeWidget(self.lb_img_volume)
        self.main_layout.removeWidget(self.time_bar)
        self.main_layout.addWidget(self.lb_img_volume, 5, 18, 1, 1)
        self.main_layout.addWidget(self.time_bar, 5, 5, 1, 13)
        self.sl_volume.setHidden(True)
        self.lb_volume.setHidden(True)

    def max(self):
        """Maximizing or minimizing window based on current state."""
        if not self.isFullScreen():
            if self.isMaximized():
                log_info("Minimizing Window.")
                if self.settings["style"] == "normal":
                    self.set_btn_icon([self.btn_max], [self.appctxt.get_resource("icons/normal/maximize.png")])
                else:
                    self.set_btn_icon([self.btn_max], [self.appctxt.get_resource("icons/darkmode/maximize.png")])
                self.showNormal()
                self.setFixedSize(650, 350)
                self.move(self.rectangle.topLeft())
            else:
                log_info("Maximizing Window.")
                if self.settings["style"] == "normal":
                    self.set_btn_icon([self.btn_max], [self.appctxt.get_resource("icons/normal/minimise.png")])
                else:
                    self.set_btn_icon([self.btn_max], [self.appctxt.get_resource("icons/darkmode/minimise.png")])
                self.showMaximized()
        else:
            log_info("Minimizing Window.")
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
            log_info("Moving Window...")
            self.move(self.x() + self.delta.x(), self.y() + self.delta.y())
            self.old_pos = event.globalPos()
            if self.old_pos == QtCore.QPoint(self.old_pos.x(), 0):
                self.max()
        elif self.isMaximized() and self.delta.y() > 0:
            self.max()

    def modify_details(self):
        """Opening window allowing to change selected track's tags."""
        log_info("Opened Modify Details.")
        self.details = ModifyDetails(list_files()[self.list.currentRow()], self)
        self.details.show()
        self.stop()

    def next(self):
        log_info("Playing Next Track.")
        self.nbr = self.list.currentRow() + 1
        if not self.list.count() == self.nbr:
            self.list.setCurrentRow(self.list.currentRow() + 1)
        else:
            self.list.setCurrentRow(0)
            self.nbr = 0
        self.play()

    def open_settings(self):
        """Reading user's settings on disc. Creates setting file if it doesn't exists with default values."""
        log_info("Reading Settings.")
        self.settings = read_settings()
        self.sl_volume.setValue(self.settings["volume"])
        if self.settings["easter_egg_on"] == True:
            self.settings["easter_egg_on"] = False
            self.easter_egg()

    def play(self):
        """Plays the selected track."""
        log_info("Playing Track " + list_files()[self.list.currentRow()] + ".")
        self.media = QtCore.QUrl.fromLocalFile(list_files()[self.list.currentRow()])
        self.file = QtMultimedia.QMediaContent(self.media)
        self.player.setMedia(self.file)
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
            log_info("Pause song.")
            self.player.pause()
            if self.player.state() == self.player.state().PausedState:
                if self.settings["style"] == "normal":
                    self.set_btn_icon([self.btn_play], [self.appctxt.get_resource("icons/normal/play.png")])
                else:
                    self.set_btn_icon([self.btn_play], [self.appctxt.get_resource("icons/darkmode/play.png")])
        elif self.player.state() == self.player.state().PausedState:
            log_info("Play song.")
            self.player.play()
            if self.player.state() == self.player.state().PlayingState:
                if self.settings["style"] == "normal":
                    self.set_btn_icon([self.btn_play], [self.appctxt.get_resource("icons/normal/pause.png")])
                else:
                    self.set_btn_icon([self.btn_play], [self.appctxt.get_resource("icons/darkmode/pause.png")])

    def refresh(self):
        log_info("Refreshing the list.")
        self.list.clear()
        self.get_musics()

    def refresh_volume(self):
        try:
            self.player.setVolume(self.settings["volume"])
            log_info("Refreshed the volume.")
        except:
            pass

    def save_settings(self):
        """Writing unsaved settings edits."""
        log_info("Saving settings.")
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
        log_info("Opened ''Set folder''.")
        self.ask = QtWidgets.QFileDialog()
        self.ask.setFileMode(self.ask.Directory)
        self.music_dir = self.ask.getExistingDirectory()
        self.settings["folder"] = self.music_dir
        self.save_settings()
        self.refresh()

    def set_time(self):
        log_info("Setting position in track.")
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
        print(self._song["title"])
        self.time_stamp = time.time()
        print(self.time_stamp)
        print(self.player.duration())
        self.max_time = time.time() + self.player.duration()/1000
        self.RPC.update(large_image="a-music-ico", details=f"Listening to " + self._song["title"], start=self.time_stamp, state=f"from " + self._song["artist"], end=self.max_time)

    def set_volume(self):
        log_info("Setting volume.")
        self.settings["volume"] = self.sl_volume.value()
        self.lb_volume.setText(f"{self.sl_volume.value()}%")
        if self.sl_volume.value() >= 75:
            self.style_.set_main_ui_slider("orange")
        elif self.sl_volume.value() < 75:
            self.style_.set_main_ui_slider("default")
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
            log_info("Showing window.")
            self.showNormal()
        else:
            log_info("Hiding window.")
            self.hide()

    def show_volume(self):
        self.main_layout.removeWidget(self.lb_img_volume)
        self.main_layout.removeWidget(self.time_bar)
        self.main_layout.addWidget(self.lb_volume, 5, 18, 1, 1)
        self.main_layout.addWidget(self.sl_volume, 5, 16, 1, 2)
        self.main_layout.addWidget(self.lb_img_volume, 5, 15, 1, 1)
        self.main_layout.addWidget(self.time_bar, 5, 5, 1, 10)
        self.sl_volume.setHidden(False)
        self.lb_volume.setHidden(False)

    def stop(self):
        """Stops the current playing song."""
        log_info("Stopping the track.")
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
            log_info("Opening Wizard")
            self.dialog = Wizard(cur_dir)
            self.dialog.exec_()
            log_info("Reading Changes")
            self.open_settings()
        else:
            pass