from PySide6.QtWidgets import QLabel, QWidget, QGraphicsOpacityEffect

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
    # 오버레이
        # 파티모집 템세팅 확인
        # 돌파고
        # 보스 패턴 알림
    # 각인 계산기
    # 경매 계산기
    # 제작 효율 계산기

    return side_bar