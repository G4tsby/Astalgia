from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QPushButton, QWidget, QGraphicsOpacityEffect, QScrollArea, QVBoxLayout, QLineEdit

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
    def __init__(self, par, character, account):
        super().__init__(par.mainwindow)
        self.todo = par
        self.character = character
        self.account = account
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

        self.load_todo()

        self.plus_btn = QPushButton("+", self)
        self.plus_btn.move(200, 50)
        self.plus_btn.setStyleSheet("font-size: 50px; color: white;")
        self.plus_btn.clicked.connect(self.plus_btn_slot)
        self.Vlayout.addWidget(self.plus_btn)

        self.temp.setLayout(self.Vlayout)
        self.scroll.setWidget(self.temp)

        self.hide()

    def load_todo(self):
        self.scroll = QScrollArea(self.window)
        self.scroll.setGeometry(0, 50, 500, 400)
        self.scroll.setStyleSheet("background-color: #282830; border-radius: 0px;")
        self.temp = QWidget(self.scroll)
        self.Vlayout = QVBoxLayout()
        self.tmp = []
        for i in range(len(self.character.todo)):
            self.tmp.append(self.Todo(self, self.character.todo[i]))
            self.Vlayout.addWidget(self.tmp[i], alignment=Qt.AlignHCenter)

    def show_todo_config(self):
        self.todo.mainwindow.hide_screen()
        self.show()
        self.raise_()

    def close_btn_slot(self):
        for i in range(len(self.character.todo)):
            self.character.todo[i]["name"] = self.tmp[i].text.text()
        self.account.save_profile()
        self.hide()
        self.todo.mainwindow.show_screen()
        self.todo.load_todo_list(self.account)
        self.deleteLater()

    def plus_btn_slot(self):
        self.character.todo.append({"name": "", "freq": 1, "icon": "카오스던전", "did": False})
        self.reload()

    def reload(self):
        for i in range(len(self.character.todo)-1):
            self.character.todo[i]["name"] = self.tmp[i].text.text()
        self.deleteLater()
        self.todo.open_config(self.character, self.account)


    class Todo(QWidget):
        def __init__(self, par, todo):
            super().__init__(par)
            self.todo = todo
            self.par = par
            self.setStyleSheet("border-radius: 0px;")
            self.setFixedSize(400, 100)
            self.back = QWidget(self)
            self.back.setStyleSheet("background-color: #282830; border: 3px solid #202027;")
            self.back.setFixedSize(400, 100)

            self.text = QLineEdit(todo["name"], self)
            self.text.move(64, 5)
            self.text.setStyleSheet("color: #ffffff; font-size: 20px; font-family: 'D2Coding';")

            self.icon = QPushButton("", self)
            self.icon.setGeometry(0, 0, 64, 64)
            self.icon.setStyleSheet(f"background: none; border-image: url(image/icon/{todo['icon']}.png);")
            self.icon.clicked.connect(self.icon_slot)

            self.delete_btn = QPushButton("삭제", self)
            self.delete_btn.setStyleSheet("font-size: 20px; color: white;")
            self.delete_btn.move(220, 5)
            self.delete_btn.clicked.connect(self.delete_btn_slot)

            self.freq_btn = []
            self.freq_btn.append(QPushButton("1일", self))
            self.freq_btn.append(QPushButton("3일", self))
            self.freq_btn.append(QPushButton("7일", self))
            for i in range(3):
                self.freq_btn[i].move(280 + i * 40, 0)
                self.freq_btn[i].setCheckable(True)
                self.freq_btn[i].clicked.connect(lambda checked=bool, idx=i: self.freq_btn_clicked(idx))
            self.freq_btn_clicked({1: 0, 3: 1, 7: 2}[todo["freq"]])

        def icon_slot(self):
            tmp = self.IconWindow(self)
            tmp.move(self.pos().x()+440, self.pos().y()+184)
            tmp.show()

        def delete_btn_slot(self):
            self.par.character.todo.remove(self.todo)
            self.deleteLater()
            self.par.reload()

        def freq_btn_clicked(self, idx):
            self.todo["freq"] = {0: 1, 1: 3, 2: 7}[idx]
            for i in range(3):
                if i != idx:
                    self.freq_btn[i].setChecked(False)
                    self.freq_btn[i].setStyleSheet("font-size: 20px; color: white; background-color: #202027;")
                else:
                    self.freq_btn[i].setChecked(True)
                    self.freq_btn[i].setStyleSheet("font-size: 20px; color: white; background-color: #abb1f4;")


        class IconWindow(QWidget):
            def __init__(self, par):
                self.todo = par
                ICON_NAME = [["카오스던전", "가디언토벌", "도전어비스", "모험섬", "발탄", "비아뽀뽀", "찬미누나", "어비스던전"],
                             ["어비스레이드", "유령선", "일일에포나", "주간에포나", "카오스게이트", "쿠크루삥뽕", "필드보스", "호감도"]]
                super().__init__(par.par)
                self.setFixedSize(328, 82)
                self.setStyleSheet("border: 3px solid #202027;")
                for i in range(2):
                    for j in range(8):
                        tmp = QPushButton("", self)
                        tmp.setFixedSize(41,41)
                        tmp.move(j * 41, i * 41)
                        tmp.setStyleSheet(f"background-color: #ffffff; border-image: url(image/icon/{ICON_NAME[i][j]}.png);")
                        tmp.clicked.connect(lambda checked=bool, a=i, b=j: self.set_icon(ICON_NAME[a][b]))

            def set_icon(self, icon):
                self.todo.todo["icon"] = icon
                self.todo.par.reload()
                self.deleteLater()


class TodoList(QWidget):
    def __init__(self, par, account):
        super().__init__(par)
        self.account = account
        self.todo = []
        self.setGeometry(0, 100, 1010, 585)
        for i in range(len(account.character)):
            self.todo.append([])
            for j in range(len(account.character[i].todo)):
                self.todo[i].append(QPushButton(self))
                self.todo[i][j].setGeometry(50 + i * 70, j * 50, 41, 41)
                self.todo[i][j].setStyleSheet(f"""
                border-image: url('./image/icon/{account.character[i].todo[j]['icon']}.png');
                background: none;
                """)
                self.todo[i][j].setCheckable(True)
                self.todo[i][j].toggled.connect(lambda checked=bool, idx=(i, j): self.todo_btn_clicked(idx))
                alpha = QGraphicsOpacityEffect(self)
                alpha.setOpacity(0.3)
                self.todo[i][j].setGraphicsEffect(alpha)
                if account.character[i].todo[j]['did'] == 1:
                    self.todo[i][j].toggle()

    def todo_btn_clicked(self, idx):
        alpha = QGraphicsOpacityEffect(self)
        if self.todo[idx[0]][idx[1]].isChecked():
            alpha.setOpacity(1)
            self.todo[idx[0]][idx[1]].setGraphicsEffect(alpha)
            self.account.character[idx[0]].todo[idx[1]]["did"] = 1
            self.account.save_profile()
        else:
            alpha.setOpacity(0.3)
            self.todo[idx[0]][idx[1]].setGraphicsEffect(alpha)
            self.account.character[idx[0]].todo[idx[1]]["did"] = 0
            self.account.save_profile()


class TodoWindow(QWidget):
    def __init__(self, par):
        super().__init__(par)
        self.mainwindow = par

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
        self.todo_list = None
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
                lambda checked=bool, a=i: self.open_config(account.character[a], account))
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
        self.load_todo_list(self.mainwindow.account[idx])

    def load_todo_list(self, account):
        self.todo_list.deleteLater() if self.todo_list is not None else None
        self.todo_list = TodoList(self, account)
        self.todo_list.show()

    def open_config(self, character, account):
        todo_config = TodoConfig(self, character, account)
        todo_config.show_todo_config()
