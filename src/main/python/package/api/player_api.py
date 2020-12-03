"""
Author: DAOUST A. @AINDUSTRIES
Project: A+Music Player
<<<<<<< HEAD
v1.4.0Pre2
=======
v1.3.0
>>>>>>> 734af32e8da76126ad3a022cc94fde045ebdcb1e
"""
from glob import glob

import os, eyed3

from package.api.settings_api import *
<<<<<<< HEAD
from package.ui.error_ui import *
=======
>>>>>>> 734af32e8da76126ad3a022cc94fde045ebdcb1e


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
<<<<<<< HEAD
    try:
        tag.save()
    except PermissionError:
        error = Error("PermissionError : Can't write tag to file.\nPlease check file premissions.")
        error.exec_()
=======
    tag.save()
>>>>>>> 734af32e8da76126ad3a022cc94fde045ebdcb1e
