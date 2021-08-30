import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont, QFontDatabase

from mainWindow import MainWindow
from expaditionData import Expadition

if __name__ == '__main__':
    app = QApplication(sys.argv)
    font = QFontDatabase()
    font.addApplicationFont("./font/NanumBarunGothic.ttf")
    app.setFont(QFont("NanumBarunGothic"))
    setting_window = MainWindow()
    sys.exit(app.exec_())
