from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QMainWindow, QPushButton, QWidget
from PyQt5.QtCore import QCoreApplication, QPoint, Qt
from todoList import TodoList

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.todo = TodoList()
        #self.setting = TodoList()
        self.initUI()

    def openTodo(self):
        self.todo.show()

    def openSetting(self):
        self.setting.show()

    def initUI(self):
        self.setWindowTitle("LoAI")
        self.resize(900, 562)
        self.setMinimumSize(900, 562)
        self.setMaximumSize(900, 562)
        self.setStyleSheet("background: rgb(29, 40, 64)")
        self.setWindowIcon(QIcon("./image/icon.png"))
        self.setWindowFlags(Qt.FramelessWindowHint)

        # 상단바
        self.bar = QWidget(self)
        self.bar.resize(900, 30)
        self.bar.setStyleSheet("background: #24314f")
        self.bar_icon = QLabel("LoAI", self)
        self.bar_icon.setStyleSheet("background: #24314f; color: white; font-weight: 400; font-size: 15px")
        self.bar_icon.move(450,0)
        self.offset = -1

        # 설정 버튼
        self.setting_button = QPushButton(self)
        self.setting_button.setStyleSheet(
            """
            QPushButton {
                border-image: url(./image/setting2.jpg);
            }
            QPushButton:pressed {
                border-image: url(./image/setting2_p.jpg);
            }
            """)
        self.setting_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setting_button.setGeometry(503, 181, 200, 200)
        self.setting_button.clicked.connect(self.openSetting)

        # 할 일 버튼
        self.todo_button = QPushButton(self)
        self.todo_button.setStyleSheet(
            """
            QPushButton {
                border-image: url(./image/todo.jpg);
            }
            QPushButton:pressed {
                border-image: url(./image/todo_p.jpg);
            }
            """)
        self.todo_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.todo_button.setGeometry(198, 181, 200, 200)
        self.todo_button.clicked.connect(self.openTodo)

        # X 버튼
        self.exit_button = QPushButton(self)
        self.exit_button.setStyleSheet(
            """
            QPushButton {
                border-image: url(./image/x.png);
            }
            QPushButton:hover {
                border-image: url(./image/x_p.jpg);
            }
            """)
        self.exit_button.setGeometry(854, 0, 46, 30)
        self.exit_button.clicked.connect(QCoreApplication.instance().quit)

        # ㅁ 버튼
        self.max_button = QPushButton(self)
        self.max_button.setStyleSheet(
            """
            QPushButton {
                border-image: url(./image/z.png);
            }
            """)
        self.max_button.setGeometry(808, 0, 46, 30)

        # _ 버튼
        self.min_button = QPushButton(self)
        self.min_button.setStyleSheet(
            """
            QPushButton {
                border-image: url(./image/M.png);
            }
            QPushButton:hover {
                border-image: url(./image/M_p.png);
            }
            """)
        self.min_button.setGeometry(762, 0, 46, 30)
        self.min_button.clicked.connect(self.showMinimized)

        self.show()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and event.pos().y() <= 30:
            self.offset = event.globalPos()
        else:
            self.offset = -1

    def mouseMoveEvent(self, event):
        if self.offset != -1:
            delta = QPoint (event.globalPos() - self.offset)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.offset = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.offset = -1
