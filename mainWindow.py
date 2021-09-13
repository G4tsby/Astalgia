from PySide6 import QtCore
from PySide6 import QtGui
from PySide6.QtGui import QIcon, QMouseEvent
from PySide6.QtWidgets import QLabel, QMainWindow, QPushButton, QWidget
from PySide6.QtCore import QCoreApplication, QPointF, Qt
#from todoList import TodoList

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setStyleSheet("font-family: NanumBarunGothic")
        self.setWindowTitle("Astalgia")
        #self.todo = TodoList()
        #self.setting = TodoList()
        self.initUI()

    def openTodo(self):
        self.todo.show()

    def openSetting(self):
        self.setting.show()

    def initUI(self):
        #self.setWindowTitle("Astalgia")
        self.resize(900, 562)
        self.setMinimumSize(900, 562)
        self.setMaximumSize(900, 562)
        self.setStyleSheet("background: #212229")
        self.setWindowIcon(QIcon("./image/4nem.png"))
        self.setWindowFlags(Qt.FramelessWindowHint)

        # 상단바
        self.bar = QWidget(self)
        self.bar.resize(900, 30)
        self.bar.setStyleSheet("background: #2f3144")
        self.bar_icon = QLabel("Astalgia", self)
        self.bar_icon.setStyleSheet("background: #2f3144; color: white; font-weight: 400; font-size: 15px;")
        self.bar_icon.move(425,0)
        self.offset = -1

        # 설정 버튼
        self.setting_button = QPushButton(self)
        self.setting_button.setStyleSheet(
            """
            QPushButton {
                border-image: url(./image/4nem.png);
            }
            QPushButton:pressed {
                border-image: url(./image/4nem_p.png);
            }
            """)
        self.setting_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setting_button.setGeometry(530, 127, 207, 220)
        self.setting_button.clicked.connect(self.openSetting)

        self.todo_text = QLabel("설정", self)
        self.todo_text.setStyleSheet("color: #b8b3e9; font-size: 25px; font-weight: 100; font-family: NanumBarunGothic")
        self.todo_text.move(235, 376)

        # 할 일 버튼
        self.todo_button = QPushButton(self)
        self.todo_button.setStyleSheet(
            """
            QPushButton {
                border-image: url(./image/todo_cube.png);
            }
            QPushButton:pressed {
                border-image: url(./image/todo_cube_p.png);
            }
            """)
        self.todo_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.todo_button.setGeometry(156, 127, 207, 227)
        self.todo_button.clicked.connect(self.openTodo)
        
        self.todo_text = QLabel("할 일", self)
        self.todo_text.setStyleSheet("color: #b8b3e9; font-size: 25px; font-weight: 100; font-family: NanumBarunGothic")
        self.todo_text.move(610, 376)

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

    def mousePressEvent(self, event:QMouseEvent):
        if event.button() == QtCore.Qt.LeftButton and event.position().y() <= 30:
            self.offset = event.globalPosition()
        else:
            self.offset = -1

    def mouseMoveEvent(self, event:QMouseEvent):
        if self.offset != -1:
            delta = QPointF(event.globalPosition() - self.offset)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.offset = event.globalPosition()

    def mouseReleaseEvent(self, event):
        self.offset = -1
