from PyQt6.uic import loadUi

from 程序文件.utils import clear_input_fields


def show_error_dialog(window, message):
    error_dialog = loadUi("ERROR.ui")
    error_dialog.ERRO.setText(message)
    error_dialog.move(1200, 400)
    error_dialog.confirm.clicked.connect(lambda: handle_error_confirmation(window, error_dialog))
    error_dialog.show()


def handle_error_confirmation(window, error_dialog):
    error_dialog.close()
    if hasattr(window, 'timer'):
        window.stop_measurement()
    clear_input_fields(window)
