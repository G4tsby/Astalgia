import os
import json

from account import Account
import topbar, sidebar, overlay, overlaywindow

from PySide6 import QtCore
from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QIcon, QMouseEvent, QPixmap
from PySide6.QtWidgets import QLabel, QMainWindow, QWidget


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
        # if not os.path.exists("preference.json"):
        #     with open("preference.json", "w") as f:
        #         json.dump({"account": []}, f)
        #
        # with open("preference.json", "rt", encoding="UTF-8") as file:
        #     config = json.load(file)
        # if len(config["account"]) != 0:
        #     self.account = [Account(i, config["account"][i]) for i in range(len(config["account"]))]
        # else:
        #     self.account = []

        # 배경
        self.background = QLabel(self)
        self.background.resize(1280, 720)
        self.background.setPixmap(QPixmap("./image/back.jpg"))
        self.background_mask = QWidget(self)
        self.background_mask.resize(1280, 720)
        self.background_mask.setStyleSheet("background: rgba(32, 32, 36, 0.85   );")

        self.setStyleSheet("background: #202024;")
        # 상단바
        top_bar = topbar.TopBar(self)
        # 좌측바
        self.side_bar = sidebar.SideBar(self)

        content = []
        # 메인 화면
        # 파티모집 템세팅 확인
        # 돌파고
        # 보스 패턴 알림
        # 생활 계산기
        ########

        # 오버레이 선택 창
        self.overlay_window = overlaywindow.OverlayWindow(self)
        self.overlay = overlay.Overlay()

        self.show()

    # 상단바 드래그로 창 옮기는 기능
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == QtCore.Qt.LeftButton and event.position().y() <= 65:
            self.offset = event.globalPosition()
        else:
            self.offset = -1

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.offset != -1:
            delta = QPointF(event.globalPosition() - self.offset)
            self.move(int(self.x() + delta.x()), int(self.y() + delta.y()))
            self.offset = event.globalPosition()

    def mouseReleaseEvent(self, event):
        self.offset = -1
