"""
Author: DAOUST A. @AINDUSTRIES
Project: A+Music Player
v1.4.0Pre2
"""
from PySide2 import QtWidgets

from package.api.player_api import *
from package.api.style_api import *

import eyed3

class ModifyDetails(QtWidgets.QWidget):

    def __init__(self, file, mainwindow):
        super().__init__()
        self.file = file
        self.mainwindow = mainwindow
        self.setup_ui()
        self.style_ = Style(self)
        self.style_.set_style()

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