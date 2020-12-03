"""
Author: DAOUST A. @AINDUSTRIES
Project: A+Music Player
v1.4.0Pre2
"""
from PySide2 import QtGui
from package.api.settings_api import *

class Style:

    def __init__(self, win):
        self.win = win

    def set_style(self):
        if read_settings()["style"] == "dark":
            self.win.setStyleSheet("""QWidget {
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
            self.win.setStyleSheet("""
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
            self.win.set_btn_icon([self.win.btn_close,
                               self.win.btn_max,
                               self.win.btn_min,
                               self.win.btn_play,
                               self.win.btn_next,
                               self.win.btn_back,
                               self.win.btn_stop,
                               self.win.btn_setts],
                              [self.win.appctxt.get_resource("icons/normal/close.png"),
                               self.win.appctxt.get_resource("icons/normal/maximize.png"),
                               self.win.appctxt.get_resource("icons/normal/min.png"),
                               self.win.appctxt.get_resource("icons/normal/play.png"),
                               self.win.appctxt.get_resource("icons/normal/next.png"),
                               self.win.appctxt.get_resource("icons/normal/back.png"),
                               self.win.appctxt.get_resource("icons/normal/stop.png"),
                               self.win.appctxt.get_resource("icons/normal/more.png")])
            self.win.pix = QtGui.QPixmap(self.win.appctxt.get_resource("icons/normal/volume.png"))
            self.win.lb_img_volume.setPixmap(self.win.pix.scaled(25, 25))
        else:
            self.win.set_btn_icon([self.win.btn_close,
                                   self.win.btn_max,
                                   self.win.btn_min,
                                   self.win.btn_play,
                                   self.win.btn_next,
                                   self.win.btn_back,
                                   self.win.btn_stop,
                                   self.win.btn_setts],
                                  [self.win.appctxt.get_resource("icons/darkmode/close.png"),
                                   self.win.appctxt.get_resource("icons/darkmode/maximize.png"),
                                   self.win.appctxt.get_resource("icons/darkmode/min.png"),
                                   self.win.appctxt.get_resource("icons/darkmode/play.png"),
                                   self.win.appctxt.get_resource("icons/darkmode/next.png"),
                                   self.win.appctxt.get_resource("icons/darkmode/back.png"),
                                   self.win.appctxt.get_resource("icons/darkmode/stop.png"),
                                   self.win.appctxt.get_resource("icons/darkmode/more.png")])
            self.win.pix = QtGui.QPixmap(self.win.appctxt.get_resource("icons/darkmode/volume.png"))
            self.win.lb_img_volume.setPixmap(self.win.pix.scaled(25, 25))

    def set_main_ui_easter_egg(self, color) -> str:
        if read_settings()["style"] == "normal":
            self.win.setStyleSheet("""
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
            self.win.setStyleSheet("""QWidget {
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
            self.win.sl_volume.setStyleSheet("""QSlider::groove:horizontal {
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
            self.win.sl_volume.setStyleSheet("""QSlider::groove:horizontal {
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
        self.win.lb_volume.setStyleSheet("QLabel { color: " + color + ";}")
        if color == "default":
            if read_settings()["style"] == "normal":
                self.win.sl_volume.setStyleSheet("""QSlider::groove:horizontal {
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
                self.win.lb_volume.setStyleSheet("QLabel { color: black;}")
            else:
                self.win.sl_volume.setStyleSheet("""QSlider::groove:horizontal {
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
                self.win.lb_volume.setStyleSheet("QLabel { color: rgb(114,137,218);}")
