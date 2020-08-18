"""
Author: DAOUST A. @AINDUSTRIES
Project: A+Music Player
v1.3.0
"""
from glob import glob

import os, eyed3

from package.api.settings_api import *


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
    tag.save()
