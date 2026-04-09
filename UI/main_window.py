from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton
)

from app.session import Session

class MainWindow(QWidget):
    def __init__(self, manager):
        super().__init__()
        self.init_UI()
        self.manager = manager

    def init_UI(self):
        self.resize(400, 200)
        self.setWindowTitle("FR:Main")

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)

        self.setLayout(self.main_layout)

    def update_user(self):
        if Session.current_user:
            if Session.current_user["role"] == "admin":
                self.reg_btn = QPushButton("New user")
                self.main_layout.addWidget(self.reg_btn)
