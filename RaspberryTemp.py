import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit
from PyQt6.QtCore import QTimer, QSettings
from PyQt6.uic import loadUi
import paramiko

class TemperatureWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = loadUi("TemperatureDetection.ui", self) # 加载 UI 文件，这里需要修改为你的UI文件路径
        self.setWindowTitle("Raspberry Pi Temperature Monitor") # 设置窗口标题

        self.timer = QTimer(self) # 创建 QTimer 实例，用于定时获取温度数据
        self.timer.timeout.connect(self.update_temperature) # 将定时器的 timeout 信号连接到更新温度数据的槽函数

        # 将按钮的点击事件连接到对应的槽函数
        self.ui.START.clicked.connect(self.start_measurement) # START 按钮
        self.ui.STOP.clicked.connect(self.stop_measurement) # STOP 按钮
        self.ui.EXIT.clicked.connect(self.exit_application) # EXIT 按钮

        # 将输入框的回车事件连接到槽函数，用于输入框之间的焦点切换
        self.ui.IPEdit.returnPressed.connect(self.ui.UserEdit.setFocus)
        self.ui.UserEdit.returnPressed.connect(self.ui.PasswordEdit.setFocus)
        self.ui.PasswordEdit.returnPressed.connect(self.start_measurement)

        self.load_settings() # 加载之前保存的设置

    def load_settings(self):
        # 从设置文件中加载 IP、用户名和密码
        settings = QSettings("MyCompany", "MyApp") # 用于保存设置的 QSettings 实例
        ip = settings.value("IP", "") # 获取之前保存的 IP 地址
        user = settings.value("User", "") # 获取之前保存的用户名
        password = settings.value("Password", "") # 获取之前保存的密码

        # 将加载的设置填充到对应的输入框中
        self.ui.IPEdit.setText(ip) # 将 IP 地址填充到 IP 输入框
        self.ui.UserEdit.setText(user) # 将用户名填充到用户名输入框
        self.ui.PasswordEdit.setText(password) # 将密码填充到密码输入框

    def save_settings(self):
        # 将当前输入框中的 IP、用户名和密码保存到设置文件中
        settings = QSettings("MyCompany", "MyApp") # 创建 QSettings 实例，用于保存设置
        settings.setValue("IP", self.ui.IPEdit.text()) # 保存当前 IP 地址
        settings.setValue("User", self.ui.UserEdit.text()) # 保存当前用户名
        settings.setValue("Password", self.ui.PasswordEdit.text()) # 保存当前密码

    def start_measurement(self):
        ip = self.ui.IPEdit.text() # 获取输入框中的 IP 地址
        user = self.ui.UserEdit.text() # 获取输入框中的用户名
        password = self.ui.PasswordEdit.text() # 获取输入框中的密码

        if not ip or not user or not password:
            print("Please enter IP, user, and password.") # 如果 IP、用户名或密码为空，打印提示信息
            return

        self.save_settings() # 保存当前输入的设置

        self.ssh = paramiko.SSHClient() # 创建 SSHClient 实例
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # 设置自动添加主机密钥的策略
        try:
            self.ssh.connect(ip, username=user, password=password) # 连接到树莓派
            self.timer.start(500)  # 启动定时器，500毫秒（0.5秒）间隔
            self.ui.START.setEnabled(False) # 连接成功后禁用 START 按钮
            self.ui.STOP.setEnabled(True) # 启用 STOP 按钮
        except paramiko.AuthenticationException:
            print("Authentication failed") # 认证失败，打印错误信息
        except paramiko.SSHException as e:
            print("SSH error:", str(e)) # SSH 连接错误，打印错误信息

    def update_temperature(self):
        try:
            stdin, stdout, stderr = self.ssh.exec_command('vcgencmd measure_temp') # 执行获取温度命令
            temperature = stdout.readlines()[0].strip() # 从输出中获取温度数据
            self.ui.lcdNumber.display(temperature) # 在 LCD 显示屏上显示温度数据
        except paramiko.SSHException as e:
            print("SSH error:", str(e)) # SSH 连接错误，打印错误信息

    def stop_measurement(self):
        self.timer.stop() # 停止定时器
        self.ui.START.setEnabled(True) # 启用 START 按钮
        self.ui.STOP.setEnabled(False) # 禁用 STOP 按钮

    def exit_application(self):
        if hasattr(self, 'ssh'):
            self.ssh.close() # 如果 SSH 连接存在，则关闭连接
        self.timer.stop() # 停止定时器
        QApplication.quit() # 退出应用程序

if __name__ == "__main__":
    app = QApplication(sys.argv) # 创建应用程序对象
    window = TemperatureWindow() # 创建主窗口对象
    window.show() # 显示主窗口
    sys.exit(app.exec()) # 运行应用程序，直到应用程序退出
