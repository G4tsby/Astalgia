from PySide6.QtWidgets import QLabel, QPushButton, QWidget, QGraphicsOpacityEffect


class SideBar(QWidget):
    def __init__(self, par):
        super().__init__(par)
        self.setGeometry(0, 65, 200, 655)
        self.setStyleSheet("background: none")
        alpha = QGraphicsOpacityEffect(self)
        alpha.setOpacity(0.24)
        self.background = QWidget(self)
        self.background.setGeometry(0, 65, 200, 655)
        self.background.setStyleSheet("background: #323238")
        self.background.setGraphicsEffect(alpha)

        # 할일
        self.todo_text = QLabel("할일", self)
        self.todo_text.setStyleSheet("background: none; color: #ffffff; font-size: 14pt; font-family: 'D2Coding';")
        self.todo_text.move(32, 230)

        self.account_button = []
        for i in range(len(par.account)):
            name = par.account[i].character[0].name
            if len(name) > 8:
                name = name[:6] + "..."
                width = (len(name) - 2) * 15 + 22
            else:
                width = len(name) * 15 + 22
            self.account_button.append(QPushButton(name, self))
            self.account_button[i].setGeometry(40, 230 + (i-1) * 30, width, 30)
            self.account_button[i].clicked.connect(self.set_account(par.account[i]))
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
        self.account_add_button.move(80, 220 + (len(par.account)-1) * 30)
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
        self.account_add_button.clicked.connect(self.add_account)
        # 오버레이
        # 파티모집 템세팅 확인
        # 돌파고
        # 보스 패턴 알림
        # 계산기
        # 각인 계산기
        # 생활 계산기
        ########

    def add_account(self):
        pass

    def set_account(self, name):
        # 시그널로 변경
        pass
