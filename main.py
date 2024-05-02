import sys
from PyQt6.QtWidgets import QApplication
from temperature_window import TemperatureWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TemperatureWindow()
    window.show()
    sys.exit(app.exec())
