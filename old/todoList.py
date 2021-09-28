import sys
import os
import json
from PySide6 import QtGui
import PySide6.QtCore
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDialog, QGridLayout, QLabel, QPushButton, QScrollArea, QTabWidget, QVBoxLayout, QWidget, QFrame, QHBoxLayout, QGraphicsBlurEffect
from expadition import Expadition

class ManageWindow(QDialog):
    def __init__(self, expadition:Expadition, config):
        super().__init__()
        self.initUI(config)
    
    def initUI(self, config):
        self.resize(800, 600)
        self.setWindowTitle("할 일 설정")

        self.account_button = []
        for i in range(config["account_count"]):
            temp = QPushButton(f"{config['account_name']}")
            temp.move(0, i*100)
            self.account_button.append(temp)


class TodoList(QWidget):
    
    ss = """
        QWidget {
            background: #212229;
            font-family: NanumBarunGothic;
        }

        QFrame {
            border: 2px solid #abb1f4;
            color: rgba(0,0,0,0);
        }

        QLabel {
            border: none
        }
    """
    def __init__(self):
        super().__init__()
        #블러 효과
        self.blur = QGraphicsBlurEffect()
        self.blur.setBlurRadius(30)

        # 저장된 계정 정보 확인후 로드 or 입력받기
        with open("preference.json", "rt", encoding="UTF-8") as file:
            self.config = json.load(file)
        if self.config["account_count"] != 0:
            expadition = [Expadition(i, self.config["account_name"][i]) for i in range(self.config["account_count"])]
        self.manage_window = ManageWindow(expadition, self.config)
        self.initUI()
    
    def account_manage(self):
        #self.setGraphicsEffect(self.blur)
        self.manage_window.show()

    def initUI(self):
        self.setWindowTitle("LoAI To do list")
        #self.setWindowIcon(QIcon("favicon.ico"))
        self.resize(1280, 720)
        self.setWindowFlags(PySide6.QtCore.Qt.FramelessWindowHint) #| PySide6.QtCore.Qt.WindowStaysOnTopHint)
        self.setStyleSheet(self.ss)

        # 한눈에 보기
        self.main_frame = QFrame(self)
        self.main_frame.setGeometry(288, 60, 970, 637)
        self.main_frame.setFrameShape(QFrame.Shape.Box)

        self.back = QLabel(self)
        self.back.setPixmap(QPixmap("./image/mokoko.png"))
        self.back.setGeometry(491, 97, 565, 564)

        # 상단바
        self.bar = QFrame(self)
        self.bar.setGeometry(288, 23, 927, 33)

        # 창 닫기
        self.exit_button = QPushButton(self)
        self.exit_button.setGeometry(1219, 23, 38, 33)
        self.exit_button.setStyleSheet("border-image: url(./image/todo_x.png)")
        self.exit_button.setCursor(QtGui.QCursor(PySide6.QtCore.Qt.PointingHandCursor))
        self.exit_button.clicked.connect(self.hide)


        # 좌상단 로고
        self.logo_frame = QFrame(self)
        self.logo_frame.setGeometry(23, 23, 257, 113)
        self.logo_frame.setStyleSheet("border: 2px solid #abb1f4")
        self.logo_image = QLabel(self)
        self.logo_image.setPixmap(QPixmap("./image/logo.png"))
        self.logo_image.setGeometry(25, 25, 252, 109)

        # 계정 목록
        self.account_button = []
        for i in range(5):
            self.account_button.append(QPushButton(self))
            self.account_button[i].setGeometry(23, 140+78*i,  257, 74)
            self.account_button[i].setStyleSheet("""
                border: 2px solid #abb1f4;
                color: #FFFFFF;
                font-size: 30px
                """)
            self.account_button[i].setCursor(QtGui.QCursor(PySide6.QtCore.Qt.PointingHandCursor))
            if self.config["account_count"] > i:
                self.account_button[i].setText(self.config["account_name"][i])
                # 할 일 목록 보이기
            else:
                self.setStyleSheet("font-size: 60px")
                self.account_button[i].setText("+")
                # 계정 추가

        # 설정
        self.setting_button = QPushButton(self)
        self.setting_button.setGeometry(23, 530, 257, 167)
        self.setting_button.setStyleSheet("border-image: url(./image/todo_setting.png)")
        self.setting_button.setCursor(QtGui.QCursor(PySide6.QtCore.Qt.PointingHandCursor))
        self.setting_button.clicked.connect(self.account_manage)
