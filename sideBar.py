from PySide6.QtWidgets import QWidget, QGraphicsOpacityEffect

def SideBar(parent):
    side_bar = QWidget(parent)
    side_bar.setGeometry(0, 65, 200, 655)
    side_bar.setStyleSheet("background: #323238")
    alpha = QGraphicsOpacityEffect(parent)
    alpha.setOpacity(0.24)
    side_bar.setGraphicsEffect(alpha)

    side_bar.offset = -1

    return side_bar