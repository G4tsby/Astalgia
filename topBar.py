from PySide6.QtWidgets import QWidget, QPushButton
from PySide6.QtCore import QCoreApplication

def TopBar(parent):
    top_bar = QWidget(parent)
    top_bar.setGeometry(0, 0, 1280, 65)
    top_bar.setStyleSheet("background: none; border-bottom: 1px solid rgba(110, 110, 110, 0.15);")

    # X 버튼
    top_bar.exit_button = QPushButton(parent)
    top_bar.exit_button.setStyleSheet(
            """
            QPushButton {
                border-image: url(./image/x.png);
            }
            QPushButton:hover {
                border-image: url(./image/x_p.jpg);
            }
            """)
    top_bar.exit_button.setGeometry(854, 0, 46, 30)
    top_bar.exit_button.clicked.connect(QCoreApplication.instance().quit)

    # ㅁ 버튼
    top_bar.max_button = QPushButton(top_bar)
    top_bar.max_button.setStyleSheet(
        """
        QPushButton {
            border-image: url(./image/z.png);
        }
        """)
    top_bar.max_button.setGeometry(808, 0, 46, 30)

    # _ 버튼
    top_bar.min_button = QPushButton(top_bar)
    top_bar.min_button.setStyleSheet(
        """
        QPushButton {
            border-image: url(./image/M.png);
        }
        QPushButton:hover {
            border-image: url(./image/M_p.png);
        }
        """)
    top_bar.min_button.setGeometry(762, 0, 46, 30)
    top_bar.min_button.clicked.connect(parent.showMinimized)

    return top_bar