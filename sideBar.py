from PySide6.QtWidgets import QLabel, QPushButton, QWidget, QGraphicsOpacityEffect


class SideBar(QWidget):
    def __init__(self, par):
        super().__init__(par)
        self.setGeometry(0, 65, 200, 655)
        self.setStyleSheet("background: none")
        alpha = QGraphicsOpacityEffect(par)
        alpha.setOpacity(0.24)
        background = QWidget(par)
        background.setGeometry(0, 65, 200, 655)
        background.setStyleSheet("background: #323238")
        background.setGraphicsEffect(alpha)

        # 할일
        todo_text = QLabel("할일", par)
        todo_text.setStyleSheet("background: none; color: #ffffff; font-size: 14pt")
        todo_text.move(32, 204)

        account_button = []
        for i in range(len(par.account)):
            name = par.account[i].character[0].name
            if len(name) > 8:
                name = name[:6] + "..."
                width = (len(name)-2) * 15 + 22
            else:
                width = len(name) * 15 + 22
            account_button.append(QPushButton(name, par))
            account_button[i].setGeometry(40, 234 + i * 30, width, 30)
            account_button[i].move(40, 234 + i * 30)
            account_button[i].setStyleSheet("""
                QPushButton {
                    background: rgba(0,0,0,0);
                    color: #ffffff;
                    font-size: 12pt;
                    text-align: left;
                    padding-left: 10px;
                }
                QPushButton:hover {
                    background: rgba(255, 255, 255, 30);
                    border-radius: 3px;
                }
                """)
        # 오버레이
        # 파티모집 템세팅 확인
        # 돌파고
        # 보스 패턴 알림
        # 계산기
        # 각인 계산기
        # 생활 계산기
