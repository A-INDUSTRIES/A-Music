"""
Author: DAOUST A. @AINDUSTRIES
Project: A+Music Player
v1.3.0 Pre3
"""
from PySide2 import QtWidgets, QtCore

class SetSpeed(QtWidgets.QWidget):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()

    def setup_ui(self):
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layout()
        self.setup_connections()

    def create_widgets(self):
        self.label = QtWidgets.QLabel("Set the playback speed:")
        self.bar = QtWidgets.QSlider()
        self.speed = QtWidgets.QLabel()
        self.btn = QtWidgets.QPushButton("Ok")

    def modify_widgets(self):
        self.bar.setRange(50, 150)
        self.bar.setValue(100)
        self.bar.setStyleSheet("""QSlider::groove:horizontal {
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
        self.bar.setOrientation(QtCore.Qt.Horizontal)
        self.bar.setSingleStep(1)
        self.bar.setPageStep(1)
        if self.main_window.sound.playbackRate() == 0.0:
            self.bar.setValue(100)
        else:
            self.bar.setValue(int(self.main_window.sound.playbackRate()*100))
        self.speed.setText("Speed: " + str(self.bar.value()))

    def create_layouts(self):
        self.layout = QtWidgets.QVBoxLayout(self)

    def add_widgets_to_layout(self):
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.bar)
        self.layout.addWidget(self.speed)
        self.layout.addWidget(self.btn)

    def setup_connections(self):
        self.btn.clicked.connect(self.close)
        self.bar.valueChanged.connect(self.set_speed)

    def set_speed(self):
        self.main_window.sound.setPlaybackRate(self.bar.value()/100)
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