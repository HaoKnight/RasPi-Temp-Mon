from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QStatusBar


class CustomStatusBar(QStatusBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.username_label = QLabel()
        self.username_label.setFont(QFont("Arial", 9, italic=True))  # 设置字号和斜体
        self.username_label.setStyleSheet("color: grey;")  # 设置颜色为蓝色
        self.addPermanentWidget(self.username_label, 1)

        self.software_label = QLabel("Software Developed By H-Knight")
        self.software_label.setFont(QFont("Arial", 9, italic=True))  # 设置字号和斜体
        self.software_label.setStyleSheet("color: grey;")  # 设置颜色为蓝色
        self.addPermanentWidget(self.software_label)

    def set_username(self, username):
        self.username_label.setText(f"  User: {username}")
