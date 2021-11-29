import os
import json
from PySide6 import QtCore
from PySide6.QtGui import QIcon, QMouseEvent, QPixmap
from PySide6.QtCore import QCoreApplication, QPointF, Qt
from PySide6.QtWidgets import QLabel, QMainWindow, QPushButton, QWidget, QGraphicsOpacityEffect

import topBar, sideBar, todo
from account import Account


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Astalgia")
        self.resize(1280, 720)
        self.setMinimumSize(1280, 720)
        self.setMaximumSize(1280, 720)
        self.setWindowIcon(QIcon("./image/4nem.png"))
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.offset = -1

        # 원정대 정보 로드
        if not os.path.exists("preference.json"):
            with open("preference.json", "w") as f:
                json.dump({"account_count": 0, "account_name": []}, f)

        with open("preference.json", "rt", encoding="UTF-8") as file:
            config = json.load(file)
        if len(config["account"]) != 0:
            self.account = [Account(i, config["account"][i]) for i in range(len(config["account"]))]
        else:
            self.account = []

        # 배경
        background = QLabel(self)
        background.resize(1280, 720)
        background.setPixmap(QPixmap("./image/back.jpg"))
        self.setStyleSheet("background: #202024;")
        alpha = QGraphicsOpacityEffect(self)
        alpha.setOpacity(0.07)
        background.setGraphicsEffect(alpha)

        # 상단바
        topBar.TopBar(self)
        # 좌측바
        sideBar.SideBar(self)
        todo.TodoWindow(self)
        content = []
        self.show()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == QtCore.Qt.LeftButton and event.position().y() <= 65:
            self.offset = event.globalPosition()
        else:
            self.offset = -1

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.offset != -1:
            delta = QPointF(event.globalPosition() - self.offset)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.offset = event.globalPosition()

    def mouseReleaseEvent(self, event):
        self.offset = -1
    