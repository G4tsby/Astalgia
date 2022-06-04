import cv2
import mss
import json
import keyboard
import numpy as np
from PIL import Image
from PySide6.QtGui import QPainter, QPen, QColor, QIcon
from PySide6.QtCore import Qt, QTimer, QThread, Signal
from PySide6.QtWidgets import QWidget, QPushButton, QApplication

pattern_activate_button = """
                QPushButton {
                    background: rgba(0,0,0,0);
                    color: rgba(0,0,0,0.5);
                    border: 0px;
                }
                QPushButton:hover {
                    color: rgba(255,255,162,0.7);
                }
                """

# 설정 로드
with open("preference.json", "r") as f:
    preference = json.load(f)
f.close()


# 설정 갱신

class Overlay(QWidget):
    def show_meteor(self):
        self.blue_meteor.toggle_visible()
        self.yellow_meteor.toggle_visible()

    def update_meteor(self):
        h = 105 / 1440 * self.h * preference["overlay"]["meteor"]["size"]
        w = 300 / 105 * h
        self.blue_meteor.setGeometry(self.w - w + preference["overlay"]["meteor"]["x"],
                                     1180 / 1440 * self.h - h + preference["overlay"]["meteor"]["y"],
                                     w, h)
        self.yellow_meteor.setGeometry(self.w - w + preference["overlay"]["meteor"]["x"],
                                       1180 / 1440 * self.h + preference["overlay"]["meteor"]["y"],
                                       w, h)
        self.blue_meteor.reload_stylesheet()
        self.yellow_meteor.reload_stylesheet()

    def update_pattern(self):
        h = 105 / 1440 * self.h * preference["overlay"]["meteor"]["size"]
        w = 300 / 105 * h
        pattern_w = w / preference["overlay"]["meteor"]["size"] * preference["overlay"]["pattern"]["size"]
        self.pattern_helper.reload(pattern_w)

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowIcon(QIcon("./image/4nem.png"))
        self.setWindowTitle("Astalgia Overlay")

        # 오버레이 단축키
        keyboard.add_hotkey('ctrl+shift+F2', lambda: self.show_meteor())
        keyboard.add_hotkey('ctrl+shift+F3', lambda: self.pattern_helper.toggle_visible())

        # 화면 크기 정보
        app = QApplication.instance()
        screen = app.primaryScreen()
        geometry = screen.availableGeometry()
        self.w, self.h = geometry.width(), geometry.height()
        self.resize(self.w, self.h)

        self.preference = preference
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
                self.origin_text = text

                self.timer = QTimer()
                self.timer.start(1000)
                self.timer.timeout.connect(self.timeout)

                self.clicked.connect(self.slot)

                self.setText(text)
                self.setGeometry(self.geo[0], self.geo[1], self.geo[2], self.geo[3])
                self.setStyleSheet(f'background: rgba({self.color[0]},{self.color[1]},{self.color[2]},0.2);\
                                    border-radius: {13 * preference["overlay"]["meteor"]["size"]}px; color: rgb{self.color};\
                                    font-size: {round(80 / 1440 * par.h * preference["overlay"]["meteor"]["size"])}px;')

            def toggle_visible(self):
                if self.isVisible():
                    self.hide()
                else:
                    self.show()

            def reload_stylesheet(self):
                self.setStyleSheet(f'background: rgba({self.color[0]},{self.color[1]},{self.color[2]},0.2);\
                                     border-radius: {13 * preference["overlay"]["meteor"]["size"]}px; color: rgb{self.color};\
                                     font-size: {round(80 / 1440 * self.par.h * preference["overlay"]["meteor"]["size"])}px;')

            def timeout(self):
                if self.status:
                    if self.text() == '0':
                        self.status = False
                        self.setText(self.origin_text)
                        self.setStyleSheet(
                            f'background: rgba({self.color[0]},{self.color[1]},{self.color[2]},0.2);\
                            border-radius: 13px; color: rgb{self.color}; \
                            font-size: {round(80 / 1440 * self.par.h * preference["overlay"]["meteor"]["size"])}px;')
                    else:
                        self.setText(str(int(self.text()) - 1))
                self.repaint()

            def slot(self):
                self.status = True
                self.setText(f"{self.time}")
                self.setStyleSheet(
                    f'background: rgba({self.color[0]},{self.color[1]},{self.color[2]},0.2);\
                    border-radius: 13px; color: rgb{self.color}; \
                    font-size: {round(100 / 1440 * self.par.h * preference["overlay"]["meteor"]["size"])}px;')

        meteor_h = 105 / 1440 * self.h * preference["overlay"]["meteor"]["size"]
        meteor_w = 300 / 105 * meteor_h
        self.blue_meteor = Meteor("파메", self, 60,
                                  (self.w - meteor_w + preference["overlay"]["meteor"]["x"],
                                   1180 / 1440 * self.h - meteor_h + preference["overlay"]["meteor"]["y"],
                                   meteor_w, meteor_h), (35, 206, 255))
        self.yellow_meteor = Meteor("노메", self, 100,
                                    (self.w - meteor_w + preference["overlay"]["meteor"]["x"],
                                     1180 / 1440 * self.h + preference["overlay"]["meteor"]["y"],
                                     meteor_w, meteor_h), (255, 209, 23))
        w, h = None, None
        self.blue_meteor.reload_stylesheet()
        self.yellow_meteor.reload_stylesheet()

        # <<<<<<<< 메테오 타이머 <<<<<<<

        # >>>>>>>> 능지패턴 족보 <<<<<<<<
        pattern_w = meteor_w / preference["overlay"]["meteor"]["size"] * preference["overlay"]["pattern"]["size"]

        class PatternHelper(QWidget):
            class Line(QPushButton):
                def __init__(self, par, angle, circle=False):
                    super().__init__(par)
                    self.par = par
                    self.angle = angle
                    self.circle = circle
                    self.enabled = False
                    self.setGeometry(par.par.w - pattern_w, 200 / 1440 * par.par.h, pattern_w, pattern_w)

                def paintEvent(self, e):
                    x, y = self.get_circle_pos()
                    qp = QPainter()
                    qp.begin(self)
                    qp.setRenderHint(QPainter.Antialiasing)
                    # if self.circle:
                    #     qp.setPen(QPen(QColor(255, 0, 0), 12 * preference["overlay"]["pattern"]["size"]))
                    #     qp.drawEllipse(0, 0,
                    #                    pattern_w * 0.7, pattern_w * 0.7)
                    #     qp.end()
                    #     return
                    if self.enabled:
                        qp.setPen(QPen(QColor(255, 255, 162), 20 * preference["overlay"]["pattern"]["size"],
                                       Qt.SolidLine, Qt.SquareCap, Qt.RoundJoin))
                        qp.drawLine(x + self.width() // 2, y + self.height() // 2, self.width() // 2,
                                    self.height() // 2)
                        qp.setPen(QPen(QColor(0, 0, 0), 12 * preference["overlay"]["pattern"]["size"],
                                       Qt.SolidLine, Qt.SquareCap, Qt.RoundJoin))
                        qp.drawLine(x + self.width() // 2, y + self.height() // 2, self.width() // 2,
                                    self.height() // 2)
                    else:
                        qp.setPen(QPen(QColor(70, 70, 70), 15 * preference["overlay"]["pattern"]["size"],
                                       Qt.SolidLine, Qt.SquareCap, Qt.RoundJoin))
                        qp.drawLine(x + self.width() // 2, y + self.height() // 2, self.width() // 2,
                                    self.height() // 2)
                    qp.end()

                def get_circle_pos(self):
                    half = self.width() * 1.2 / 2
                    x = half * np.sin(np.radians(self.angle))
                    y = half * np.cos(np.radians(self.angle))
                    return x, y

                def off(self):
                    self.enabled = False
                    self.repaint()

                def on(self):
                    self.enabled = True
                    self.repaint()

            class ActivateButton(QPushButton):
                def __init__(self, par, x, n):
                    super().__init__(par)
                    self.n = n
                    self.par = par
                    self.setGeometry(x, 200 / 1440 * par.par.h + pattern_w / 3 * 2, pattern_w / 3, pattern_w / 3)
                    self.setStyleSheet(pattern_activate_button)
                    self.clicked.connect(self.slot)

                def slot(self):
                    if self.n == 7:
                        if 7 in self.par.activated:
                            self.par.activated.remove(7)
                        else:
                            self.par.activated.append(7)
                    elif self.n == 6:
                        if 6 in self.par.activated:
                            self.par.activated.remove(6)
                        else:
                            self.par.activated.append(6)
                    elif self.n == 5:
                        if 5 in self.par.activated:
                            self.par.activated.remove(5)
                        else:
                            self.par.activated.append(5)

                    if set(self.par.activated) not in [{5, 6, 7}, {6, 7}, {5, 7}, {6}]:
                        temp = []
                        for i in [5, 6, 7]:
                            if i in self.par.activated:
                                temp.append(i)
                        self.par.activated = temp
                    if set(self.par.activated) == {5, 6, 7}:
                        self.par.activated = [11, 1, 5, 6, 7]
                    elif set(self.par.activated) == {5, 7}:
                        self.par.activated = [11, 1, 5, 7, 3]
                    elif set(self.par.activated) == {6, 7}:
                        self.par.activated = [1, 6, 7, 3, 9]
                    elif set(self.par.activated) == {6}:
                        self.par.activated = [11, 1, 3, 9, 6]

                    for key, value in self.par.lines.items():
                        if key in self.par.activated:
                            value.on()
                        else:
                            value.off()

            class Circle(QWidget):
                def __init__(self, par):
                    super().__init__(par)

                    self.par = par
                    self.pattern_w = pattern_w
                    self.setGeometry(par.par.w - pattern_w, 200 / 1440 * par.par.h, pattern_w, pattern_w)

                def reload(self, new_w):
                    self.pattern_w = new_w
                    self.setGeometry(self.par.par.w - new_w, 200 / 1440 * self.par.par.h, new_w, new_w)
                    self.repaint()

                def paintEvent(self, e):
                    qp = QPainter()
                    qp.begin(self)
                    qp.setRenderHint(QPainter.Antialiasing)
                    qp.setPen(QPen(QColor(255, 255, 255), 12 * preference["overlay"]["pattern"]["size"]))
                    qp.drawEllipse(self.pattern_w * 0.15, self.pattern_w * 0.15,
                                   self.pattern_w * 0.7, self.pattern_w * 0.7)
                    qp.end()

            def __init__(self, par):
                super().__init__(par)

                self.par = par
                self.activated = []

                self.background = QWidget(self)
                self.background.setGeometry(par.w - pattern_w, 200 / 1440 * par.h, pattern_w, pattern_w)
                self.background.setStyleSheet("background: rgba(0,0,0,0.7);")
                self.circle = self.Circle(self)
                self.lines = {
                    1: self.Line(self, 135),
                    3: self.Line(self, 90),
                    5: self.Line(self, 45),
                    6: self.Line(self, 0),
                    7: self.Line(self, -45),
                    9: self.Line(self, -90),
                    11: self.Line(self, -135)
                }

                self.activate_buttons = {
                    5: self.ActivateButton(self, par.w - pattern_w / 3, 5),
                    6: self.ActivateButton(self, par.w - pattern_w / 3 * 2, 6),
                    7: self.ActivateButton(self, par.w - pattern_w, 7)
                }

            def reload(self, new_w):
                for i in self.lines.values():
                    i.setGeometry(self.par.w - new_w, 200 / 1440 * self.par.h, new_w, new_w)
                for i in range(len(self.activate_buttons.values())):
                    self.activate_buttons[i + 5].setGeometry(self.par.w - new_w / 3 * (i + 1),
                                                             200 / 1440 * self.par.h + new_w / 3 * 2, new_w / 3,
                                                             new_w / 3)
                self.circle.reload(new_w)
                self.background.setGeometry(self.par.w - new_w, 200 / 1440 * self.par.h, new_w, new_w)

            def toggle_visible(self):
                if self.isVisible():
                    self.hide()
                else:
                    self.show()

        self.pattern_helper = PatternHelper(self)
        # <<<<<<<< 능지패턴 족보 <<<<<<<


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
