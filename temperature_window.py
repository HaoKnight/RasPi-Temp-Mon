from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QLineEdit, QMessageBox, QApplication
from PyQt6.QtWidgets import QMainWindow
from PyQt6.uic import loadUi

from error_dialog import show_error_dialog
from settings import load_settings, save_settings
from ssh_client import SSHClient
from status_bar import CustomStatusBar
from theme import ThemeManager


class TemperatureWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ssh = None
        self.ui = loadUi("TemperatureDetection.ui", self)
        self.setWindowTitle("Raspberry Pi Temperature Monitor")

        self.ui.TEMP.mousePressEvent = self.toggle_theme

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_temperature)

        self.ui.START.clicked.connect(self.start_measurement)
        self.ui.STOP.clicked.connect(self.stop_measurement)
        self.ui.EXIT.clicked.connect(self.exit_application)

        self.ui.IPEdit.returnPressed.connect(self.ui.UserEdit.setFocus)
        self.ui.UserEdit.returnPressed.connect(self.ui.PasswordEdit.setFocus)
        self.ui.PasswordEdit.returnPressed.connect(self.start_measurement)
        self.ui.PasswordEdit.setEchoMode(QLineEdit.EchoMode.Password)
        load_settings(self)

        self.status_bar = CustomStatusBar()
        self.setStatusBar(self.status_bar)

        if self.ui.IPEdit.text() and self.ui.UserEdit.text() and self.ui.PasswordEdit.text():
            self.start_measurement()

    @staticmethod
    def toggle_theme(event):
        ThemeManager.toggle_theme()

    def start_measurement(self):
        ip = self.ui.IPEdit.text()
        user = self.ui.UserEdit.text()
        password = self.ui.PasswordEdit.text()

        if not ip or not user or not password:
            QMessageBox.warning(self, "Warning", "Please enter IP, user, and password.")
            return

        save_settings(self)

        try:
            self.ssh = SSHClient(ip, user, password)
            self.ssh.connect()
            self.timer.start(500)
            self.ui.START.setEnabled(False)
            self.ui.STOP.setEnabled(True)
        except Exception as ex:
            show_error_dialog(self, str(ex))

        self.status_bar.set_username(user)

    def update_temperature(self):
        try:
            temperature = self.ssh.get_temperature()
            self.ui.lcdNumber.display(temperature)
        except Exception as ex:
            show_error_dialog(self, str(ex))

    def stop_measurement(self):
        self.timer.stop()
        self.ui.START.setEnabled(True)
        self.ui.STOP.setEnabled(False)

    def exit_application(self):
        if hasattr(self, 'ssh'):
            self.ssh.close()
        self.timer.stop()
        QApplication.quit()
