from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QSettings
from PyQt6.QtGui import QPalette, QColor


class ThemeManager:
    @staticmethod
    def toggle_theme():
        app = QApplication.instance()

        # 获取当前主题状态
        current_theme = ThemeManager.get_current_theme()

        # 切换主题
        if current_theme == "light":
            ThemeManager.set_dark_theme()
        elif current_theme == "dark":
            ThemeManager.set_light_theme()

    @staticmethod
    def set_dark_theme():
        app = QApplication.instance()
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, QColor(30, 30, 30))
        dark_palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, QColor(30, 30, 30))
        dark_palette.setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, QColor(30, 30, 30))
        dark_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, QColor(128, 128, 128))
        app.setPalette(dark_palette)

        # 保存主题设置
        settings = QSettings("MyCompany", "MyApp")
        settings.setValue("Theme", "dark")

    @staticmethod
    def set_light_theme():
        app = QApplication.instance()
        light_palette = QPalette()

        # 设置活动窗口的背景颜色和文本颜色
        # 设置活动窗口的背景颜色为白色，文本颜色为黑色
        light_palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, QColor(255, 255, 255))
        light_palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, QColor(0, 0, 0))

        # 设置非活动窗口的背景颜色为白色，文本颜色为黑色
        light_palette.setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, QColor(255, 255, 255))
        light_palette.setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, QColor(0, 0, 0))

        # 设置禁用状态窗口的背景颜色为浅灰色，文本颜色为深灰色
        light_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, QColor(240, 240, 240))
        light_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, QColor(128, 128, 128))

        app.setPalette(light_palette)

        # 保存主题设置
        settings = QSettings("MyCompany", "MyApp")
        settings.setValue("Theme", "light")

    @staticmethod
    def get_current_theme():
        app = QApplication.instance()
        settings = QSettings("MyCompany", "MyApp")
        return settings.value("Theme", "light")


