from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QPushButton, QLabel, QGraphicsOpacityEffect


# 오버레이 선택 창
class OverlayWindow(QWidget):
    # 기능 버튼 공용 클래스
    class OverlayButton(QPushButton):
        def __init__(self, parent, geometry: tuple, text, n):
            super().__init__(parent)
            self.overlay_window = parent
            self.status = False

            self.alpha = QGraphicsOpacityEffect(self)
            self.alpha.setOpacity(0.5)
            self.setGeometry(geometry[0], geometry[1], geometry[2], geometry[3])
            self.setStyleSheet(f"background: rgba(50,50,56, 0.8); border-radius: 13px;")
            self.setGraphicsEffect(self.alpha)
            self.clicked.connect(lambda: self.slot(n))

            self.image = QLabel(self)
            self.image.setStyleSheet("background: none")
            self.text = QLabel(text, self)
            self.text.setStyleSheet("color: white; font-size: 30px;background: none")
            self.show()

        # 각 버튼 클릭시 호출됨
        def slot(self, n):
            # 활성화 상태일때
            if self.status:
                self.alpha.setOpacity(0.5)
                self.status = False
                if n == 0:
                    self.overlay_window.mainwindow.overlay.pattern_helper.toggle_visible()
                elif n == 1:
                    self.overlay_window.mainwindow.overlay.blue_meteor.toggle_visible()
                    self.overlay_window.mainwindow.overlay.yellow_meteor.toggle_visible()
            # 비활성화 상태일때
            else:
                self.alpha.setOpacity(1)
                self.status = True
                if n == 0:
                    self.overlay_window.mainwindow.overlay.pattern_helper.toggle_visible()
                elif n == 1:
                    self.overlay_window.mainwindow.overlay.blue_meteor.toggle_visible()
                    self.overlay_window.mainwindow.overlay.yellow_meteor.toggle_visible()

    def __init__(self, par):
        super().__init__(par)
        self.mainwindow = par
        self.setGeometry(235, 100, 1010, 585)

        self.alpha = QGraphicsOpacityEffect(self)
        self.alpha.setOpacity(0.8)

        self.background = QWidget(self)
        self.background.setGeometry(0, 50, 1010, 585)
        self.background.setStyleSheet("background: rgba(38,38,42,0.75); border-radius: 13px;")

        self.boss = self.OverlayButton(self, (150, 100, 200, 200), "능지 족보", 0)
        self.boss.image.setPixmap(QPixmap("image/boss.png").scaledToWidth(120, Qt.SmoothTransformation))
        self.boss.image.move(40, 20)
        self.boss.text.move(40, 140)

        self.meteor = self.OverlayButton(self, (400, 100, 200, 200), "운석 타이머", 1)
        self.meteor.image.setPixmap(QPixmap("image/meteor.png").scaledToWidth(120, Qt.SmoothTransformation))
        self.meteor.image.move(40, 20)
        self.meteor.text.move(20, 140)

        self.checker = self.OverlayButton(self, (650, 100, 200, 200), " 커밍쑨", 2)
        self.checker.image.setPixmap(QPixmap("image/backpack.png").scaledToHeight(110, Qt.SmoothTransformation))
        self.checker.image.move(55, 20)
        self.checker.text.move(38, 140)