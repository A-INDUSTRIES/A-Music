"""
Author: DAOUST A. @AINDUSTRIES
Project: A+Music Player
<<<<<<< HEAD
v1.4.0Pre2
=======
v1.3.0
>>>>>>> 734af32e8da76126ad3a022cc94fde045ebdcb1e
"""
from PySide2 import QtWidgets
from package.api.style_api import *

class About(QtWidgets.QMessageBox):

    def __init__(self):
        super().__init__()
        self.style_ = Style(self)
        self.style_.set_style()
        self.setWindowTitle("A+Music | About")
        self.setText("""A+Music is a basic music player wich is now playing only mp3.
        This app is open-sourced. Therefore, you can edit the code as you wish.
        This app has been developped by a teenager who is learning.
        If you read this, you're God!
        (Also, click once on the "A" of A+Music...)
        (You can click another time on it to disable the thing.)


        ΔINDUSTRIES.""")