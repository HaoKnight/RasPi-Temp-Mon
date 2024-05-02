from PyQt6.QtWidgets import QStatusBar, QLabel
from PyQt6.QtCore import QSettings
from PyQt6.QtGui import QFont
class Settings:
    def __init__(self, main_window):
        self.settings = QSettings("MyCompany", "MyApp") # 用于保存设置的 QSettings 实例
        self.main_window = main_window

    def save(self, ip, user, password):
        # 将当前输入框中的 IP、用户名和密码保存到设置文件中
        self.settings.setValue("IP", ip) # 保存当前 IP 地址
        self.settings.setValue("User", user) # 保存当前用户名
        self.settings.setValue("Password", password) # 保存当前密码

    def load(self):
        # 从设置文件中加载 IP、用户名和密码
        ip = self.settings.value("IP", "") # 获取之前保存的 IP 地址
        user = self.settings.value("User", "") # 获取之前保存的用户名
        password = self.settings.value("Password", "") # 获取之前保存的密码
        return ip, user, password

    def setup_status_bar(self):
        # 创建状态栏
        status_bar = QStatusBar()
        status_bar.setStyleSheet("background-color: transparent;")  # 设置状态栏背景色为透明色
        self.main_window.setStatusBar(status_bar)

        # 显示登录的用户名
        user_label = QLabel("  User: " + self.main_window.ui.UserEdit.text())
        status_bar.addPermanentWidget(user_label, stretch=1)
        user_label_font = QFont()
        user_label.setStyleSheet("color: grey;")  # 设置文本颜色为白色
        user_label_font.setPointSize(9)  # 设置字体大小为 12
        user_label_font.setItalic(True)  # 设置为斜体
        user_label.setFont(user_label_font)

        # 显示 "Software Developed By H-Knight"
        software_label = QLabel(" Software Developed By H-Knight ")
        status_bar.addPermanentWidget(software_label)
        software_label_font = QFont()  # 创建字体对象
        software_label.setStyleSheet("color: grey;")  # 设置文本颜色为白色
        software_label_font.setPointSize(8)  # 设置字体大小为 10
        software_label_font.setItalic(True)  # 设置为斜体
        software_label.setFont(software_label_font)