from PySide6.QtWidgets import QLabel, QWidget, QGraphicsOpacityEffect

def SideBar(parent):
    side_bar = QWidget(parent)
    side_bar.setGeometry(0, 65, 200, 655)
    side_bar.setStyleSheet("background: none")

    alpha = QGraphicsOpacityEffect(parent)
    alpha.setOpacity(0.24)
    side_bar.backgound = QWidget(parent)
    side_bar.backgound.setGeometry(0, 65, 200, 655)
    side_bar.backgound.setStyleSheet("background: #323238")
    side_bar.backgound.setGraphicsEffect(alpha)

    return side_bar