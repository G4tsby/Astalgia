from PySide6.QtWidgets import QWidget, QPushButton, QGraphicsOpacityEffect, QLabel, QApplication
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QTimer
from tkinter import Tk
import keyboard


class OverlayWindow(QWidget):
    class OverlayButton(QPushButton):
        def __init__(self, parent, g:tuple, text, n):
            super().__init__(parent)
            self.overlaywindow = parent
            self.status = False
            self.al = QGraphicsOpacityEffect(self)
            self.al.setOpacity(0.5)
            self.setGeometry(g[0], g[1], g[2], g[3])
            self.setStyleSheet(f"background: rgba(50,50,56, 0.8); border-radius: 13px;")
            self.setGraphicsEffect(self.al)
            self.clicked.connect(lambda :self.slot(n))
            self.image = QLabel(self)
            self.image.setStyleSheet("background: none")
            self.text = QLabel(text, self)
            self.text.setStyleSheet("color: white; font-size: 30px;background: none")
            self.show()

        def slot(self, n):
            if self.status:
                self.al.setOpacity(0.5)
                self.status = False
                if n == 0:
                    pass
                elif n == 1:
                    self.overlaywindow.mainwindow.overlay.blue_meteor.hide()
                    self.overlaywindow.mainwindow.overlay.yellow_meteor.hide()

            else:
                self.al.setOpacity(1)
                self.status = True
                if n == 0:
                    pass
                elif n == 1:
                    self.overlaywindow.mainwindow.overlay.blue_meteor.show()
                    self.overlaywindow.mainwindow.overlay.yellow_meteor.show()

    def __init__(self, par):
        super().__init__(par)
        self.mainwindow = par
        self.setGeometry(235, 100, 1010, 585)

        self.alpha = QGraphicsOpacityEffect(self)
        self.alpha.setOpacity(0.8)

        preset = 100
        self.background = QWidget(self)
        self.background.setGeometry(0, 50, 1010, 585)
        self.background.setStyleSheet("background: rgba(38,38,42,0.75); border-radius: 13px;")

        self.boss = self.OverlayButton(self, (150, 100, 200, 200), "패턴 알림", 0)
        self.boss.image.setPixmap(QPixmap("image/boss.png").scaledToWidth(120, Qt.SmoothTransformation))
        self.boss.image.move(40, 20)
        self.boss.text.move(40, 140)

        self.meteor = self.OverlayButton(self, (400, 100, 200, 200), "운석 타이머", 1)
        self.meteor.image.setPixmap(QPixmap("image/meteor.png").scaledToWidth(120, Qt.SmoothTransformation))
        self.meteor.image.move(40, 20)
        self.meteor.text.move(20, 140)

        self.checker = self.OverlayButton(self, (650, 100, 200, 200), "군장검사", 2)
        self.checker.image.setPixmap(QPixmap("image/backpack.png").scaledToHeight(110, Qt.SmoothTransformation))
        self.checker.image.move(55, 20)
        self.checker.text.move(38, 140)

class Overlay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        #keyboard.add_hotkey('ctrl+shift+F2', lambda: print("@@@@@"))

        app = QApplication.instance()
        screen = app.primaryScreen()
        geometry = screen.availableGeometry()
        self.w, self.h = geometry.width(), geometry.height()

        self.timer = QTimer()
        self.timer.timeout.connect(self.yellow_timeout)
        self.timer.start(1000)
        self.yellow_status = False
        self.blue_status = False

        self.resize(self.w, self.h)
        # 2560 1440
        # 1920 1080
        # 1707 912
        # meteor
        self.yellow_meteor = QPushButton("노메", self)
        y_h = 105/1440*self.h
        y_w = 300/105*y_h
        self.yellow_meteor.setGeometry(self.w-y_w, 1180/1440*self.h, y_w, y_h)
        self.yellow_meteor.setStyleSheet(f"background: rgba(255,209,23,0.2); border-radius: 13px; color: rgb(255,209,23); font-size: {round(80/1440*self.h)}px;")
        self.yellow_meteor.clicked.connect(lambda: self.timer_slot(0))
        self.yellow_meteor.hide()

        self.blue_meteor = QPushButton("파메", self)
        self.blue_meteor.setGeometry(2260, 1075, 300, 105)
        self.blue_meteor.setGeometry(self.w - y_w, 1180 / 1440 * self.h-y_h, y_w, y_h)
        self.blue_meteor.setStyleSheet(f"background: rgba(35,206,255,0.2); border-radius: 13px; color: rgb(35,206,255); font-size: {round(80/1440*self.h)}px;")
        self.blue_meteor.clicked.connect(lambda: self.timer_slot(1))
        self.blue_meteor.hide()


        if 1.7 < self.w/self.h < 1.8:
            print("Running on 16:9")
        elif 2.3 < self.w/self.h < 2.4:
            print("Running on 21:9")

        self.show()

    def activate(self, n):
        pass

    def timer_slot(self, n):
        if n == 0:
            self.yellow_status = True
            self.yellow_meteor.setText("100")
            self.yellow_meteor.setStyleSheet(f"background: rgba(255,209,23,0.2); border-radius: 13px; color: rgb(255,209,23); font-size: {round(100/1440*self.h)}px;")
        elif n == 1:
            self.blue_status = True
            self.blue_meteor.setText("60")
            self.blue_meteor.setStyleSheet(f"background: rgba(35,206,255,0.2); border-radius: 13px; color: rgb(35,206,255); font-size: {round(100/1440*self.h)}px;")

    def yellow_timeout(self):
        if self.yellow_status:
            if self.yellow_meteor.text() == '0':
                self.yellow_status = False
                self.yellow_meteor.setText("노메")
                self.yellow_meteor.setStyleSheet(f"background: rgba(255,209,23,0.2); border-radius: 13px; color: rgb(255,209,23); font-size: {round(80/1440*self.h)}px;")
            else:
                self.yellow_meteor.setText(str(int(self.yellow_meteor.text()) - 1))
        if self.blue_status:
            if self.blue_meteor.text() == '0':
                self.blue_status = False
                self.blue_meteor.setText("파메")
                self.blue_meteor.setStyleSheet(f"background: rgba(35,206,255,0.2); border-radius: 13px; color: rgb(35,206,255); font-size: {round(80/1440*self.h)}px;")
            else:
                self.blue_meteor.setText(str(int(self.blue_meteor.text()) - 1))
        self.repaint()


