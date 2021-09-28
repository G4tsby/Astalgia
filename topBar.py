from PySide6.QtWidgets import QWidget, QPushButton, QLabel
from PySide6.QtCore import QCoreApplication

def TopBar(parent):
    top_bar = QWidget(parent)
    top_bar.setGeometry(0, 0, 1280, 65)
    top_bar.setStyleSheet("background: none; border-bottom: 1px solid rgba(110, 110, 110, 0.15);")

    # 로고
    logo = QWidget(parent)
    logo.setGeometry(17, 11, 40, 43)
    logo.setStyleSheet("border-image: url(./image/4nem_mini.png); background: none;")
    logo_text = QLabel("Astalgia", parent)
    logo_text.setGeometry(70, 15, 150, 35)
    logo_text.setStyleSheet("font-size: 18pt; color: #abb1f4; background: none;")


    # X 버튼
    top_bar.exit_button = QPushButton(parent)
    top_bar.exit_button.setStyleSheet(
            """
            QPushButton {
                border-image: url(./image/exit.png);
            }
            QPushButton:hover {
                border-image: url(./image/exit_p.png);
            }
            """)
    top_bar.exit_button.setGeometry(1215, 15, 35, 35)
    top_bar.exit_button.clicked.connect(QCoreApplication.instance().quit)

    # ㅁ 버튼
    top_bar.max_button = QPushButton(top_bar)
    top_bar.max_button.setStyleSheet(
        """
        QPushButton {
            border-image: url(./image/max.png);
        }
        """)
    top_bar.max_button.setGeometry(1180, 15, 35, 35)

    # _ 버튼
    top_bar.min_button = QPushButton(top_bar)
    top_bar.min_button.setStyleSheet(
        """
        QPushButton {
            border-image: url(./image/min.png);
        }
        QPushButton:hover {
            border-image: url(./image/min_p.png);
        }
        """)
    top_bar.min_button.setGeometry(1145, 15, 35, 35)
    top_bar.min_button.clicked.connect(parent.showMinimized)

    return top_bar