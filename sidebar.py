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

        self.setGeometry(0, 65, 200, 655)
        alpha = QGraphicsOpacityEffect(self)
        alpha.setOpacity(0.24)

        self.background = QWidget(self)
        self.background.setGeometry(0, 0, 200, 655)
        self.background.setStyleSheet("background: #323238")
        self.background.setGraphicsEffect(alpha)

        # 오버레이
        self.overlay_setting = QLabel("오버레이 설정", self)
        self.overlay_setting.setStyleSheet("background: none; color: #ffffff; font-size: 14pt; font-family: 'D2Coding';")
        self.overlay_setting.move(32, 165)

        self.meteor = QPushButton("운석 타이머", self)
        self.meteor.setGeometry(30, 195, 150, 30)
        self.meteor.setStyleSheet(default_menu_text)
        self.meteor.clicked.connect(lambda: self.sidebar_slot("meteor"))

        self.pattern = QPushButton("능지 족보", self)
        self.pattern.setGeometry(30, 225, 150, 30)
        self.pattern.setStyleSheet(default_menu_text)
        self.pattern.clicked.connect(lambda: self.sidebar_slot("pattern"))

    def sidebar_slot(self, type: str):
        if type == "meteor":
            self.mainwindow.overlay_window.hide()
            self.mainwindow.content["meteor"].show()
            self.mainwindow.content["pattern"].hide()
        elif type == "pattern":
            self.mainwindow.overlay_window.hide()
            self.mainwindow.content["pattern"].show()
            self.mainwindow.content["meteor"].hide()
