"""
Author: DAOUST A. @AINDUSTRIES
Project: A+Music Player
v1.3.0
"""
import logging, os

def __init__():
    log_file = os.path.join(os.path.join(os.path.expanduser("~"), "A+Music"), "latest_log.txt")
    logging.basicConfig(level=logging.INFO, filename=log_file, filemode="w",
                    format='%(asctime)s - %(levelname)s - %(message)s')

def log_info(arg):
    logging.info(arg)
