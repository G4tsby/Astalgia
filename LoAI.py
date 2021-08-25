import os
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QApplication, QDesktopWidget, QMainWindow, QPushButton, QWidget, qApp

import expaditionData

if __name__ == '__main__':
    #name = input()
    name = "행복관NPC"
    expadition = expaditionData.Expadition(name)
    #print(expadition.character[0].name, expadition.character[0].level, expadition.character[0].item_level)