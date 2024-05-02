from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import QTimer, QSettings
from PyQt6.uic import loadUi
from settings import Settings
from ssh_manager import SSHManager

class TemperatureWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = loadUi("TemperatureDetection.ui", self)  # 加载 UI 文件，这里需要修改为你的UI文件路径
        self.setWindowTitle("Raspberry Pi Temperature Monitor")  # 设置窗口标题

        self.timer = QTimer(self)  # 创建 QTimer 实例，用于定时获取温度数据
        self.timer.timeout.connect(self.update_temperature)  # 将定时器的 timeout 信号连接到更新温度数据的槽函数

        # 将按钮的点击事件连接到对应的槽函数
        self.ui.START.clicked.connect(self.start_measurement)  # START 按钮
        self.ui.STOP.clicked.connect(self.stop_measurement)  # STOP 按钮
        self.ui.EXIT.clicked.connect(self.exit_application)  # EXIT 按钮

        # 将输入框的回车事件连接到槽函数，用于输入框之间的焦点切换
        self.ui.IPEdit.returnPressed.connect(self.ui.UserEdit.setFocus)
        self.ui.UserEdit.returnPressed.connect(self.ui.PasswordEdit.setFocus)
        self.ui.PasswordEdit.returnPressed.connect(self.start_measurement)

        # 设置密码输入框显示为 *
        self.ui.PasswordEdit.setEchoMode(QLineEdit.EchoMode.Password)

        self.settings = Settings(self)  # 创建 Settings 实例，用于保存和加载设置
        self.load_settings()  # 加载之前保存的设置
        self.settings.setup_status_bar()  # 设置状态栏

    def load_settings(self):
        ip, user, password = self.settings.load() # 从设置文件中加载 IP、用户名和密码
        self.ui.IPEdit.setText(ip) # 将 IP 地址填充到 IP 输入框
        self.ui.UserEdit.setText(user) # 将用户名填充到用户名输入框
        self.ui.PasswordEdit.setText(password) # 将密码填充到密码输入框

    def start_measurement(self):
        ip = self.ui.IPEdit.text() # 获取输入框中的 IP 地址
        user = self.ui.UserEdit.text() # 获取输入框中的用户名
        password = self.ui.PasswordEdit.text() # 获取输入框中的密码

        if not ip or not user or not password:
            print("Please enter IP, user, and password.") # 如果 IP、用户名或密码为空，打印提示信息
            return

        self.settings.save(ip, user, password) # 保存当前输入的设置

        self.ssh_manager = SSHManager(ip, user, password) # 创建 SSHManager 实例，用于管理 SSH 连接
        self.timer.start(500)  # 启动定时器，500毫秒（0.5秒）间隔
        self.ui.START.setEnabled(False) # 连接成功后禁用 START 按钮
        self.ui.STOP.setEnabled(True) # 启用 STOP 按钮

    def update_temperature(self):
        temperature = self.ssh_manager.get_temperature() # 获取温度数据
        self.ui.lcdNumber.display(temperature) # 在 LCD 显示屏上显示温度数据

    def stop_measurement(self):
        self.timer.stop() # 停止定时器
        self.ui.START.setEnabled(True) # 启用 START 按钮
        self.ui.STOP.setEnabled(False) # 禁用 STOP 按钮

    def exit_application(self):
        self.ssh_manager.close() # 关闭 SSH 连接
        self.timer.stop() # 停止定时器
        self.close() # 关闭窗口
