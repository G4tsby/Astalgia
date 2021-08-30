import sys
import os
import json
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont, QFontDatabase 

from mainWindow import MainWindow
from expaditionData import Expadition

if __name__ == '__main__':
    app = QApplication(sys.argv)
    font = QFontDatabase()
    font.addApplicationFont("./font/NanumBarunGothic.ttf")
    app.setFont(QFont("NanumBarunGothic"))
    #<로딩화면>

    # 저장된 원정대 정보 확인
    expadition = []
    with open("preference.json", "rt", encoding="UTF-8") as file:
        config = json.load(file)
    if config["account_count"] != 0:
        expadition = [Expadition(i, config["account_character"][i]) for i in range(config["account_count"])]
    setting_window = MainWindow(expadition)
    sys.exit(app.exec_())