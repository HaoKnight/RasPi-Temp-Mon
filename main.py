import sys

from PyQt6.QtWidgets import QApplication

from temperature_window import TemperatureWindow
from theme import ThemeManager

if __name__ == "__main__":

    app = QApplication(sys.argv)
    ThemeManager.set_dark_theme()
    window = TemperatureWindow()
    window.show()
    sys.exit(app.exec())