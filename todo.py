from PySide6.QtCore import Slot
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QPushButton, QWidget, QGraphicsOpacityEffect
import account as acc

X_OFFSET = 50


class TodoWindow(QWidget):
    def __init__(self, par):
        super().__init__(par)
        # 캐릭터별 할 일 위젯(열)
        #  self.char[캐릭터][0: 직업이미지 1: 캐릭터 이름 2:캐릭터 레벨 3~ 할일]
        self.char = []

        #### UI INIT ####
        self.setGeometry(235, 100, 1010, 585)

        # 알파 효과
        alpha = QGraphicsOpacityEffect(self)
        alpha.setOpacity(0.75)

        # 배경
        self.background = QWidget(self)
        self.background.setGeometry(0, 0, 1010, 585)
        self.background.setStyleSheet("background: #26262a; border-radius: 13px;")
        self.background.setGraphicsEffect(alpha)

        # 가로 구분선
        self.partition = QWidget(self)
        self.partition.setGeometry(0, 0, 1010, 80)
        self.partition.setStyleSheet("background: none; border-bottom: 2px solid rgba(110, 110, 110, 0.34);")

        self.acc = []
        for i in range(len(par.account)):
            self.add_account(par.account[i])

    def add_account(self, account: acc):
        self.acc.append([])
        idx = len(self.acc) - 1
        for i in range(len(account.character)):
            self.acc[idx].append([])
            # 직업 아이콘
            self.acc[idx][i].append(QLabel(self))
            self.acc[idx][i][0].setPixmap(QPixmap(f"image/class/{account.character[i].clss}").scaled(41, 41))
            self.acc[idx][i][0].setStyleSheet("background: none;")
            self.acc[idx][i][0].setGeometry(X_OFFSET + i * 70, 10, 41, 41)
            icon_location = self.acc[idx][i][0].frameGeometry()
            icon_location = icon_location.x() + icon_location.width() / 2

            # 닉네임
            if len(account.character[i].name) > 6:
                name = account.character[i].name[:6]
            else:
                name = account.character[i].name
            self.acc[idx][i].append(QLabel(name, self))
            text_location = self.acc[idx][i][1].fontMetrics().boundingRect(self.acc[idx][i][1].text()).width() / 2
            self.acc[idx][i][1].move(icon_location - text_location + 3, 55)
            self.acc[idx][i][1].setStyleSheet("background: none; color: white; font-family: NanumBarunGothic;")

            self.acc[idx][i][0].hide()
            self.acc[idx][i][1].hide()

    def set_account(self, idx):
        for i in range(len(self.acc)):
            for j in range(len(self.acc[i])):
                if i == idx:
                    self.acc[i][j][0].show()
                    self.acc[i][j][1].show()
                else:
                    self.acc[i][j][0].hide()
                    self.acc[i][j][1].hide()