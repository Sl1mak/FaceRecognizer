import sys

from UI.login_window import LoginWindow
from UI.register_window import RegisterWindow
from UI.main_window import MainWindow
from PyQt5.QtWidgets import QApplication
from app.database import get_connection

class WindowManager:
    def __init__(self):
        self.login_window = LoginWindow(self)
        self.register_window = RegisterWindow(self)
        self.main_window = MainWindow(self)

        self.windows = {
            "login": self.login_window,
            "register": self.register_window,
            "main": self.main_window,
        }

    def switch(self, window_name):
        for window in self.windows.values():
            window.hide()
        self.windows[window_name].show()
        self.windows[window_name].update_user()

if __name__ == '__main__':
    con = get_connection()
    app = QApplication(sys.argv)
    manager = WindowManager()
    manager.switch("login")
    sys.exit(app.exec())