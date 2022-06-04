import json
from PySide6.QtWidgets import QLabel, QPushButton, QWidget

from topbar import control_button

# 설정 파일 로드
with open("preference.json", "r") as f:
    preference = json.load(f)

# 인덱스 별 크기 배율
INDEX = [0.5, 1, 1.5, 2]
SIZE = {0.5: 0, 1: 1, 1.5: 2, 2: 3}


def size_button(color: str):
    return f"""
            color: white;
            font-size: 20px;
            font-family: 'NanumBarunGothic';
            background: {color};
            border: none;
            """


# 메테오 타이머 설정
class MeteorPatternSetting(QWidget):
    class SizeButton(QPushButton):
        def __init__(self, par, num):
            super().__init__(par)
            self.num = num
            self.par = par
            self.status = False
            self.setGeometry(125, 145, 60, 40)
            self.clicked.connect(self.size_slot)

        def size_slot(self):
            for i in range(len(self.par.widget_size)):
                self.par.widget_size[i].off()
            self.on()
            preference["overlay"][self.par.obj]["size"] = INDEX[self.num]
            self.par.mainwindow.overlay.preference["overlay"][self.par.obj]["size"] = INDEX[self.num]
            if self.par.obj == "meteor":
                self.par.mainwindow.overlay.update_meteor()
            elif self.par.obj == "pattern":
                self.par.mainwindow.overlay.update_pattern()

        def off(self):
            self.setStyleSheet(size_button("#202024"))
            self.status = False

        def on(self):
            self.setStyleSheet(size_button("#abb1f4"))
            self.status = True

    def __init__(self, par, obj):
        super().__init__(par,)
        self.obj = obj
        self.mainwindow = par
        self.setGeometry(235, 100, 1010, 585)

        self.size = preference["overlay"][obj]["size"]
        self.x, self.y = preference["overlay"][obj]["x"], preference["overlay"][obj]["y"]

        self.background = QWidget(self)
        self.background.setGeometry(0, 50, 1010, 585)
        self.background.setStyleSheet("background: rgba(38,38,42,0.75); border-radius: 13px; ")

        # X 버튼
        self.exit_button = QPushButton(self)
        self.exit_button.setStyleSheet(control_button("exit"))
        self.exit_button.setGeometry(960, 65, 35, 35)
        self.exit_button.clicked.connect(self.exit)

        if obj == "meteor":
            self.title = QLabel("메테오 타이머 설정", self)
        elif obj == "pattern":
            self.title = QLabel("능지 족보 설정", self)
        self.title.setStyleSheet("color: white; font-size: 20px; background: none; font-family: 'NanumBarunGothic'")

        self.widget_size_text = QLabel("위젯 크기", self)
        self.widget_size_text.setStyleSheet("color: white; font-size: 20px;background: none; font-family: 'NanumBarunGothic';")
        self.widget_size_text.setGeometry(85, 145, 400, 40)

        self.widget_size = []
        for i in range(4):
            self.widget_size.append(self.SizeButton(self, i))
            self.widget_size[i].setGeometry(180 + i * 65, 145, 60, 40)
            self.widget_size[i].setText(str(INDEX[i]))
            self.widget_size[i].setStyleSheet(size_button("#202024"))
        self.widget_size[SIZE[self.size]].on()

        self.hide()

    def exit(self):
        self.hide()
        self.mainwindow.overlay_window.show()
        with open("preference.json", "w") as f:
            json.dump(preference, f, indent=4)