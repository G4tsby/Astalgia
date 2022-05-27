import cv2
import mss
import keyboard
import numpy as np
from PIL import Image
from PySide6.QtCore import Qt, QTimer, QThread, Signal
from PySide6.QtWidgets import QWidget, QPushButton, QApplication


class Overlay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        keyboard.add_hotkey('ctrl+shift+F2', lambda: self.show_meteor())

        app = QApplication.instance()
        screen = app.primaryScreen()
        geometry = screen.availableGeometry()
        self.w, self.h = geometry.width(), geometry.height()

        if 1.7 < self.w / self.h < 1.9:
            print("Running on 16:9")
        elif 2.3 < self.w / self.h < 2.4:
            print("Running on 21:9")

        self.resize(self.w, self.h)
        self.show()

        # 2560 1440
        # 1920 1080
        # 1707 912

        # >>>>>>>> 메테오 타이머 >>>>>>>>
        class Meteor(QPushButton):
            def __init__(self, text, par, time, geo, color: tuple):
                super().__init__(par)

                self.par = par
                self.geo = geo
                self.time = time
                self.color = color
                self.status = False

                self.timer = QTimer()
                self.timer.start(1000)
                self.timer.timeout.connect(self.timeout)

                self.clicked.connect(self.slot)

                self.setText(text)
                self.setGeometry(self.geo[0], self.geo[1], self.geo[2], self.geo[3])
                self.setStyleSheet(f"""background: rgba({self.color[0]},{self.color[1]},{self.color[2]},0.2);
                border-radius: 13px; color: rgb{self.color}; font-size: {round(80 / 1440 * par.h)}px;""")

            def toggle_visible(self):
                if self.isVisible():
                    self.hide()
                else:
                    self.show()

            def timeout(self):
                if self.status:
                    if self.text() == '0':
                        self.status = False
                        self.setText("노메")
                        self.setStyleSheet(
                            f"""background: rgba({self.color[0]},{self.color[1]},{self.color[2]},0.2);
                            border-radius: 13px; color: rgb{self.color}; font-size: {round(80 / 1440 * self.par.h)}px;""")
                    else:
                        self.setText(str(int(self.text()) - 1))
                self.repaint()

            def slot(self):
                self.status = True
                self.setText(f"{self.time}")
                self.setStyleSheet(
                    f"""background: rgba({self.color[0]},{self.color[1]},{self.color[2]},0.2);
                    border-radius: 13px; color: rgb{self.color}; font-size: {round(100 / 1440 * self.par.h)}px;""")

        meteor_h = 105 / 1440 * self.h
        meteor_w = 300 / 105 * meteor_h
        self.yellow_meteor = Meteor("노메", self, 100,
                                    (self.w - meteor_w, 1180 / 1440 * self.h, meteor_w, meteor_h), (255, 209, 23))
        self.blue_meteor = Meteor("파메", self, 80,
                                  (self.w - meteor_w, 1180 / 1440 * self.h - meteor_h, meteor_w, meteor_h), (35, 206, 255))
        # <<<<<<<< 메테오 타이머 <<<<<<<



class ScreenReader(QThread):
    timeout = Signal(str)

    def __init__(self, w, h):
        super().__init__()
        mon = {f'top': 0, 'left': 0, 'width': {w}, 'height': {h}}
        capture = mss.mss()
        capture_img = capture.grab(mon)
        img = Image.frombytes('RGB', (capture_img.size.width, capture_img.size.height), capture_img.rgb)
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    def run(self):
        pass
