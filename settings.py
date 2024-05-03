from PyQt6.QtCore import QSettings


def load_settings(window):
    settings = QSettings("MyCompany", "MyApp")
    ip = settings.value("IP", "")
    user = settings.value("User", "")
    password = settings.value("Password", "")

    window.ui.IPEdit.setText(ip)
    window.ui.UserEdit.setText(user)
    window.ui.PasswordEdit.setText(password)


def save_settings(window):
    settings = QSettings("MyCompany", "MyApp")
    settings.setValue("IP", window.ui.IPEdit.text())
    settings.setValue("User", window.ui.UserEdit.text())
    settings.setValue("Password", window.ui.PasswordEdit.text())


def set_username(self, username):
    self.username_label.setText("Username: " + username)
