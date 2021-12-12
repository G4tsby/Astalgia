from PySide6.QtWidgets import QLabel, QPushButton, QWidget, QGraphicsOpacityEffect, QScrollArea, QVBoxLayout, QFrame

# 할 일 관리창 스타일시트
SCROLL_STYLE = """
    QScrollArea {
        background-color: #242428;
    }
    QScrollBar:vertical {
     background: #181820;
     width: 15px;
    }
    QScrollBar::handle:vertical {
        background: gray;
        min-height: 20px;
    }
     QScrollBar::add-line:vertical {
         height: 0px;
     }
     QScrollBar::sub-line:vertical {
         height: 0px;
     }
     QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
         background: none;
     }
"""


class TodoConfig(QWidget):
    class Todo(QWidget):
        def __init__(self, par, todo):
            super().__init__(par)
            self.todo = todo
            self.back = QWidget(self)
            self.back.setStyleSheet("background-color: #282830; border: 3px solid #202027;")
            self.back.setFixedSize(400, 100)

            self.text = QLabel(todo["name"], self)
            self.text.move(64, 0)
            self.text.setStyleSheet("color: #ffffff; font-size: 20px; font-family: 'D2Coding';")

            self.icon = QPushButton("", self)
            self.icon.setGeometry(0, 0, 64, 64)
            self.icon.setStyleSheet(f"background: none; border-image: url(image/icon/{todo['icon']}.png);")

            self.delete_btn = QPushButton("삭제", self)
            self.delete_btn.setStyleSheet("font-size: 20px; color: white;")
            self.delete_btn.move(220, 0)

            self.freq_btn = []
            self.freq_btn.append(QPushButton("1일", self))
            self.freq_btn.append(QPushButton("3일", self))
            self.freq_btn.append(QPushButton("7일", self))
            for i in range(3):
                self.freq_btn[i].move(280 + i * 40, 0)
                self.freq_btn[i].setCheckable(True)
                self.freq_btn[i].clicked.connect(lambda checked=bool, idx=i: self.freq_btn_clicked(idx))
            self.freq_btn_clicked({1: 0, 3: 1, 7: 2}[todo["freq"]])

        def freq_btn_clicked(self, idx):
            self.todo["freq"] = {0: 1, 1: 3, 2: 7}[idx]
            for i in range(3):
                if i != idx:
                    self.freq_btn[i].setChecked(False)
                    self.freq_btn[i].setStyleSheet("font-size: 20px; color: white; background-color: #202027;")
                else:
                    self.freq_btn[i].setChecked(True)
                    self.freq_btn[i].setStyleSheet("font-size: 20px; color: white; background-color: #abb1f4;")

    def __init__(self, par, character):
        super().__init__(par.mainwindow)
        self.todo = par
        self.resize(1280, 720)
        self.setStyleSheet(SCROLL_STYLE)

        self.window = QWidget(self)
        self.window.resize(500, 600)
        self.window.move(440, 60)
        self.window.setStyleSheet("border-radius: 10px;")

        self.title = QLabel(f'{character.name} 할일 관리', self.window)
        self.title.setStyleSheet("font-size: 20px; color: white;")

        self.cancel = QPushButton('닫기', self.window)
        self.cancel.move(200, 500)
        self.cancel.clicked.connect(self.close_btn_slot)
        self.cancel.setStyleSheet("font-size: 20px; color: white;")

        self.scroll = QScrollArea(self.window)
        self.scroll.setGeometry(0, 50, 500, 400)
        self.scroll.setStyleSheet("background-color: #282830; border-radius: 0px;")
        self.temp = QWidget()
        # self.temp.setStyleSheet("background: none;")
        self.layout = QVBoxLayout()
        ##test###
        character.todo = [{'name': '카던', "icon": "카오스던전", "freq": 1}]
        ########
        for i in range(len(character.todo)):
            self.tmp = self.Todo(self, character.todo[i])
            self.tmp.setFixedSize(400, 64)
            self.tmp.setStyleSheet("border-radius: 0px;")
            self.layout.addWidget(self.tmp)

        self.temp.setLayout(self.layout)
        self.scroll.setWidget(self.temp)

        self.hide()

    def show_todo_config(self):
        self.todo.mainwindow.hide_screen()
        self.show()
        self.raise_()

    def close_btn_slot(self):
        self.hide()
        self.todo.mainwindow.show_screen()
        self.deleteLater()


class TodoWindow(QWidget):
    def __init__(self, par):
        super().__init__(par)
        self.mainwindow = par
        # 캐릭터별 할 일 위젯(열)
        #  self.char[캐릭터][0: 직업이미지 1: 캐릭터 이름 2:캐릭터 레벨 3~ 할일]
        self.char = []

        #### UI INIT ####
        self.setGeometry(235, 100, 1010, 585)
        # 알파 효과
        alpha = QGraphicsOpacityEffect(self)
        alpha.setOpacity(0.75)

        # 할 일  설정 창

        # 배경
        self.background = QWidget(self)
        self.background.setGeometry(0, 0, 1010, 585)
        self.background.setStyleSheet("background: #26262a; border-radius: 13px;")
        self.background.setGraphicsEffect(alpha)

        # 가로 구분선
        self.partition = QWidget(self)
        self.partition.setGeometry(0, 0, 1010, 80)
        self.partition.setStyleSheet("background: none; border-bottom: 2px solid rgba(110, 110, 110, 0.34);")

        self.acc = []
        for i in range(len(par.account)):
            self.add_account(par.account[i])

    def add_account(self, account):
        self.acc.append([])
        idx = len(self.acc) - 1
        for i in range(len(account.character)):
            self.acc[idx].append([])
            # 직업 아이콘
            self.acc[idx][i].append(QPushButton(self))
            self.acc[idx][i][0].setStyleSheet(
                f"background: none; border-image: url(image/class/{account.character[i].clss}.png);")
            self.acc[idx][i][0].setGeometry(50 + i * 70, 10, 41, 41)
            self.acc[idx][i][0].clicked.connect(
                lambda checked=bool, a=i: self.open_config(account.character[a]))
            icon_location = self.acc[idx][i][0].frameGeometry()
            icon_location = icon_location.x() + icon_location.width() / 2

            # 닉네임
            if len(account.character[i].name) > 6:
                name = account.character[i].name[-6:]
            else:
                name = account.character[i].name
            self.acc[idx][i].append(QLabel(name, self))
            text_location = self.acc[idx][i][1].fontMetrics().boundingRect(self.acc[idx][i][1].text()).width() / 2
            self.acc[idx][i][1].move(icon_location - text_location + 3, 55)
            self.acc[idx][i][1].setStyleSheet("background: none; color: white; font-family: NanumBarunGothic;")

            self.acc[idx][i][0].hide()
            self.acc[idx][i][1].hide()

    def set_account(self, idx):
        for i in range(len(self.acc)):
            for j in range(len(self.acc[i])):
                if i == idx:
                    self.acc[i][j][0].show()
                    self.acc[i][j][1].show()
                else:
                    self.acc[i][j][0].hide()
                    self.acc[i][j][1].hide()

    def open_config(self, character):
        todo_config = TodoConfig(self, character)
        todo_config.show_todo_config()
        todo_config = None
