import json
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QPushButton, QWidget, QGraphicsOpacityEffect, QLineEdit

from account import Account


class AddAccount(QWidget):
    def __init__(self, par):
        super().__init__(par.mainwindow)
        self.sidebar = par
        self.resize(1280, 720)

        self.window = QWidget(self)
        self.window.resize(400, 400)
        self.window.move(440, 160)
        self.window.setStyleSheet("border-radius: 10px;")

        self.title = QLabel('계정 추가', self.window)
        self.title.setStyleSheet("font-size: 20px; color: white;")

        self.name = QLineEdit(self.window)
        self.name.move(100, 100)
        self.name.setStyleSheet("background-color:#ffffff")

        self.add = QPushButton('확인', self.window)
        self.add.move(100, 350)
        self.add.clicked.connect(self.confirm_btn_slot)
        self.add.setStyleSheet("font-size: 20px; color: white;")

        self.cancel = QPushButton('취소', self.window)
        self.cancel.move(150, 350)
        self.cancel.clicked.connect(self.cancel_btn_slot)
        self.cancel.setStyleSheet("font-size: 20px; color: white;")

        self.hide()

    def confirm_btn_slot(self):
        self.sidebar.mainwindow.account.append(Account(len(self.sidebar.mainwindow.account), self.name.text()))

        with open("preference.json", "rt", encoding="UTF-8") as file:
            config = json.load(file)
            config["account"].append(self.name.text())
        with open("preference.json", "w") as file:
            json.dump(config, file)

        self.sidebar.mainwindow.to_do.add_account(self.sidebar.mainwindow.account[-1])
        self.sidebar.add_account(self.sidebar, self.sidebar.mainwindow.account[-1].character[0].name)
        self.close()
        self.sidebar.mainwindow.show_screen()

    def show_window(self):
        self.sidebar.mainwindow.hide_screen()
        self.show()
        self.raise_()

    def cancel_btn_slot(self):
        self.close()
        self.sidebar.mainwindow.show_screen()



class SideBar(QWidget):

    def __init__(self, par):
        self.mainwindow = par
        super().__init__(self.mainwindow)

        #### UI INIT ####
        self.setGeometry(0, 65, 200, 655)
        self.setStyleSheet("background: none")
        alpha = QGraphicsOpacityEffect(self)
        alpha.setOpacity(0.24)

        self.add = AddAccount(self)

        self.background = QWidget(self)
        self.background.setGeometry(0, 0, 200, 655)
        self.background.setStyleSheet("background: #323238")
        self.background.setGraphicsEffect(alpha)

        # 할일
        self.todo_text = QLabel("할일", self)
        self.todo_text.setStyleSheet("background: none; color: #ffffff; font-size: 14pt; font-family: 'D2Coding';")
        self.todo_text.move(32, 165)

        self.account_button = []
        for i in range(len(self.mainwindow.account)):
            name = self.mainwindow.account[i].character[0].name
            if len(name) > 8:
                name = name[:6] + "..."
                width = (len(name) - 2) * 15 + 22
            else:
                width = len(name) * 15 + 22
            self.account_button.append(QPushButton(name, self))
            self.account_button[i].setGeometry(40, 195 + i * 30, width, 30)
            self.account_button[i].clicked.connect(lambda checked=bool, n=i: self.mainwindow.to_do.set_account(n))
            self.account_button[i].setStyleSheet("""
                                        QPushButton {
                                            background: rgba(0,0,0,0);
                                            color: rgba(255,255,255,0.5);
                                            font-size: 12pt;
                                            text-align: left;
                                            padding-left: 10px;
                                        }
                                        QPushButton:hover {
                                            color: #ffffff;
                                        }
                                        """)

        self.account_add_button = QPushButton("+", self)
        self.account_add_button.move(80, 195 + len(self.mainwindow.account) * 30)
        self.account_add_button.setStyleSheet("""
                                                        QPushButton {
                                                            background: rgba(0,0,0,0);
                                                            color: rgba(255,255,255,0.5);
                                                            font-size: 24pt;
                                                            text-align: center;
                                                            padding-bottom: 3px;
                                                        }
                                                        QPushButton:hover {
                                                            color: #ffffff;
                                                        }
                                                        """)
        self.account_add_button.clicked.connect(self.add.show_window)
        # toggled
        # background: rgba(255, 255, 255, 30);
        # border - radius: 3px;

        # 오버레이
        # 파티모집 템세팅 확인
        # 돌파고
        # 보스 패턴 알림
        # 계산기
        # 각인 계산기
        # 생활 계산기
        ########
    # 사이드바에 새로운 계정 추가
    def add_account(self, sidebar, name):
        self.account_button.append(QPushButton(name, sidebar))
        i = len(self.account_button) - 1

        if len(name) > 8:
            name = name[:6] + "..."
            width = (len(name) - 2) * 15 + 22
        else:
            width = len(name) * 15 + 22
        self.account_button[i].setGeometry(40, 195 + i * 30, width, 30)
        self.account_button[i].clicked.connect(lambda checked=bool, n=i: self.mainwindow.to_do.set_account(n))
        self.account_button[i].setStyleSheet("""
                                                    QPushButton {
                                                        background: rgba(0,0,0,0);
                                                        color: rgba(255,255,255,0.5);
                                                        font-size: 12pt;
                                                        text-align: left;
                                                        padding-left: 10px;
                                                    }
                                                    QPushButton:hover {
                                                        color: #ffffff;
                                                    }
                                                    """)
        self.account_button[i].show()
        self.account_add_button.move(80, 195 + (i+1) * 30)