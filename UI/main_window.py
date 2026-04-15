from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton
)

from app.session import Session
from app.queries import getModels

class MainWindow(QWidget):
    def __init__(self, manager):
        super().__init__()
        self.init_UI()
        self.manager = manager

    def init_UI(self):
        self.resize(200, 200)
        self.setWindowTitle("FR:Main")

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(10)

        self.start_btn = QPushButton("Start")
        self.main_layout.addWidget(self.start_btn)
        self.setting_btn = QPushButton("Settings")
        self.main_layout.addWidget(self.setting_btn)

        self.setting_btn.clicked.connect(lambda: self.manager.show("settings"))

        self.setLayout(self.main_layout)

    def update_user(self):
        if Session.current_user:
            if Session.current_user["role"] == "admin":
                self.reg_btn = QPushButton("New user")
                self.main_layout.addWidget(self.reg_btn)
                self.manager.models_list = getModels(Session.current_user["user_id"])
                print(Session.current_user["user_id"])
                print(self.manager.models_list)

