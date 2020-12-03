"""
Author: DAOUST A. @AINDUSTRIES
Project: A+Music Player
v1.4.0Pre2
"""
from PySide2 import QtWidgets

from package.api.style_api import *

class Error(QtWidgets.QMessageBox):

    def __init__(self, error):
        super().__init__()
        self.setText(error)
        self._style = Style(self)
        self._style.set_style()
