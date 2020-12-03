"""
Author: DAOUST A. @AINDUSTRIES
Project: A+Music Player
<<<<<<< HEAD
v1.4.0Pre2
=======
v1.3.0
>>>>>>> 734af32e8da76126ad3a022cc94fde045ebdcb1e
"""
import logging, os

def __init__():
    log_file = os.path.join(os.path.join(os.path.expanduser("~"), "A+Music"), "latest_log.txt")
    logging.basicConfig(level=logging.INFO, filename=log_file, filemode="w",
                    format='%(asctime)s - %(levelname)s - %(message)s')

def log_info(arg):
    logging.info(arg)
