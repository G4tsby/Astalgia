import os
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QApplication, QDesktopWidget, QMainWindow, QPushButton, QWidget, qApp

import expaditionData

if __name__ == '__main__':
    name = input()
    expadition = expaditionData.Expadition(name)