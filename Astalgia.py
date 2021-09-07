import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont, QFontDatabase
import logging
from datetime import datetime
from mainWindow import MainWindow

if __name__ == '__main__':
    logger = logging.getLogger()

    app = QApplication(sys.argv)
    QFontDatabase.addApplicationFont("./font/NanumBarunGothic.ttf")
    setting_window = MainWindow()
    sys.exit(app.exec())