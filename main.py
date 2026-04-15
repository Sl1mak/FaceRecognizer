import sys

from PyQt5.QtWidgets import QApplication
from app.database import get_connection
from app.manager import WindowManager

if __name__ == '__main__':
    con = get_connection()
    app = QApplication(sys.argv)
    manager = WindowManager()
    manager.switch("login")
    sys.exit(app.exec())