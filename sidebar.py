from PySide6.QtWidgets import QLabel, QPushButton, QWidget, QGraphicsOpacityEffect

default_menu_text = """
                QPushButton {
                    background: rgba(0,0,0,0);
                    color: rgba(255,255,255,0.5);
                    font-size: 12pt;
                    text-align: left;
                    padding-left: 10px;
                    font-family: 'NanumBarunGothic';
                }
                QPushButton:hover {
                    color: #ffffff;
                }
                """

class SideBar(QWidget):
    def __init__(self, par):
        self.mainwindow = par
        super().__init__(self.mainwindow)

        #### UI INIT ####
        self.setGeometry(0, 65, 200, 655)
        self.setStyleSheet("background: none")
        alpha = QGraphicsOpacityEffect(self)
        alpha.setOpacity(0.24)

        self.background = QWidget(self)
        self.background.setGeometry(0, 0, 200, 655)
        self.background.setStyleSheet("background: #323238")
        self.background.setGraphicsEffect(alpha)



        # 오버레이
        self.todo_text = QLabel("오버레이", self)
        self.todo_text.setStyleSheet("background: none; color: #ffffff; font-size: 14pt; font-family: 'D2Coding';")
        self.todo_text.move(32, 165)

        self.meteor = QPushButton("운석 타이머", self)
        self.meteor.setGeometry(40, 195, 50, 30)
        self.meteor.setStyleSheet(default_menu_text)
