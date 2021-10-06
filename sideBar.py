from PySide6.QtWidgets import QLabel, QPushButton, QWidget, QGraphicsOpacityEffect

def SideBar(parent):
    side_bar = QWidget(parent)
    side_bar.setGeometry(0, 65, 200, 655)
    side_bar.setStyleSheet("background: none")

    alpha = QGraphicsOpacityEffect(parent)
    alpha.setOpacity(0.24)
    side_bar.backgound = QWidget(parent)
    side_bar.backgound.setGeometry(0, 65, 200, 655)
    side_bar.backgound.setStyleSheet("background: #323238")
    side_bar.backgound.setGraphicsEffect(alpha)

    # 할일
    side_bar.todo_text = QLabel("할일", parent)
    side_bar.todo_text.setStyleSheet("background: none; color: #ffffff; font-size: 14pt")
    side_bar.todo_text.move(32, 204)
    
    side_bar.account_button = []
    for i in range(len(parent.account)):
        side_bar.account_button.append(QPushButton(parent, parent.account[i].character[0].name))
        side_bar.account_button[i].move(50, 304+i*100)
        side_bar.account_button.setStyleSheet("background: none; color: #ffffff; font-size: 12pt")
    # 오버레이
        # 파티모집 템세팅 확인
        # 돌파고
        # 보스 패턴 알림
    # 각인 계산기
    # 경매 계산기
    # 제작 효율 계산기