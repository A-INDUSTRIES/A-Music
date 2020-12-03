"""
Author: DAOUST A. @AINDUSTRIES
Project: A+Music Player
v1.4.0Pre2
"""
from PySide2 import QtWidgets, QtCore

from package.api.settings_api import *


import json
import os

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
        self.page2_layout = QtWidgets.QGridLayout(self.page2)
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
        self.page3 = QtWidgets.QWizardPage()
        self.page3.setTitle("Quick Setup")
        self.page3.setSubTitle("Done!\nThe app is now ready to go!")

    def add_pages(self):
        self.addPage(self.page1)
        self.addPage(self.page2)
        self.addPage(self.page3)

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