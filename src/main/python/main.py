"""
Author: DAOUST A. @AINDUSTRIES
Project: A+Music Player
v1.3.0 Pre2
"""
from fbs_runtime.application_context.PySide2 import ApplicationContext
from package.main_window import MainWindow

import sys

if __name__ == '__main__':
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    window = MainWindow(appctxt)
    window.showNormal()
    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
