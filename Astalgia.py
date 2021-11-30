import sys
import logging
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase

import mainwindow


if __name__ == '__main__':
    logger = logging.getLogger()
    app = QApplication(sys.argv)
    QFontDatabase.addApplicationFont("./font/NanumBarunGothic.ttf")
    QFontDatabase.addApplicationFont("./font/D2Coding.ttc")
    window = mainwindow.MainWindow()
    sys.exit(app.exec())
