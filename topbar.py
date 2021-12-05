from PySide6.QtWidgets import QWidget, QPushButton, QLabel
from PySide6.QtCore import QCoreApplication


class TopBar(QWidget):
    def __init__(self, par):
        super().__init__(par)
        self.setGeometry(0, 0, 1280, 65)
        self.background = QWidget(self)
        self.background.setGeometry(0, 0, 1280, 65)
        self.background.setStyleSheet("background: none; border-bottom: 1px solid rgba(110, 110, 110, 0.15);")

        # 로고
        self.logo = QWidget(self)
        self.logo.setGeometry(17, 11, 40, 43)
        self.logo.setStyleSheet("border-image: url(./image/4nem_mini.png); background: none;")
        self.logo_text = QLabel("Astalgia", self)
        self.logo_text.setGeometry(70, 15, 150, 35)
        self.logo_text.setStyleSheet("font-size: 18pt; color: #abb1f4; background: none;")

        # X 버튼
        self.exit_button = QPushButton(self)
        self.exit_button.setStyleSheet(
            """
            QPushButton {
                border-image: url(./image/exit.png);
            }
            QPushButton:hover {
                border-image: url(./image/exit_p.png);
            }
            """)
        self.exit_button.setGeometry(1215, 15, 35, 35)
        self.exit_button.clicked.connect(QCoreApplication.instance().quit)

        # ㅁ 버튼
        self.max_button = QPushButton(self)
        self.max_button.setStyleSheet(
            """
            QPushButton {
                border-image: url(./image/max.png);
            }
            """)
        self.max_button.setGeometry(1180, 15, 35, 35)

        # _ 버튼
        self.min_button = QPushButton(self)
        self.min_button.setStyleSheet(
            """
            QPushButton {
                border-image: url(./image/min.png);
            }
            QPushButton:hover {
                border-image: url(./image/min_p.png);
            }
            """)
        self.min_button.setGeometry(1145, 15, 35, 35)
        self.min_button.clicked.connect(par.showMinimized)