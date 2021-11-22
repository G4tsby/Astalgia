import sys
import logging
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase

import mainWindow


if __name__ == '__main__':
    logger = logging.getLogger()
    app = QApplication(sys.argv)
    QFontDatabase.addApplicationFont("./font/NanumBarunGothic.ttf")
    window = mainWindow.MainWindow()
    sys.exit(app.exec())
