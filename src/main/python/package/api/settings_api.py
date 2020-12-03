"""
Author: DAOUST A. @AINDUSTRIES
Project: A+Music Player
<<<<<<< HEAD
v1.4.0Pre2
=======
v1.3.0
>>>>>>> 734af32e8da76126ad3a022cc94fde045ebdcb1e
"""
import os, json

cur_dir = os.path.join(os.path.expanduser("~"), "A+Music")
# Gets the folder where setting file is gonna be.

def create_settings():
    os.makedirs(os.path.join(cur_dir, ""), exist_ok=True)
    with open(os.path.join(cur_dir, "settings.json"), "w") as a:
        settings = {"folder": "C:/Users/pc/Music", "volume": 100, "easter_egg_on": False, "configured": False,
                    "style": "normal"}
        json.dump(settings, a)

def read_settings():
    if not os.path.exists(os.path.join(cur_dir, "settings.json")):
        create_settings()
    with open(os.path.join(cur_dir, "settings.json"), "r") as f:
        settings = json.load(f)
        try:
            if settings["style"]:
                return settings
        except KeyError:
            create_settings()
            with open(os.path.join(cur_dir, "settings.json"), "r") as f:
                return json.load(f)


def write_settings(settings) -> list:
    with open(os.path.join(cur_dir, "settings.json"), "w") as c:
        json.dump(settings, c)