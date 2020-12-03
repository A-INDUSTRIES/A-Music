"""
Author: DAOUST A. @AINDUSTRIES
Project: A+Music Player
v1.4.0Pre2
"""
from PySide2 import QtWidgets, QtCore
from package.api.style_api import *
from package.api.settings_api import *

class Settings(QtWidgets.QWidget):

    def __init__(self, main_window):
        super().__init__()
        self.settings = read_settings()
        self.main_window = main_window
        self.setup_ui()
        self.style_ = Style(self)
        self.style_.set_style()

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
        self.style_.set_style()
        self.main_window.style_.set_style()
        self.main_window.style_.set_main_ui_icons()
        self.main_window.settings = read_settings()