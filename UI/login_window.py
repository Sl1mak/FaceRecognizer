from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QGroupBox, QPushButton, QMessageBox,
)

from app.queries import login
from app.session import Session

from UI.help_window import HelpWindow

class LoginWindow(QWidget):
    def __init__(self, manager):
        super().__init__()
        self.init_UI()
        self.manager = manager
        self.help_window = HelpWindow(self.manager)

    def init_UI(self):
        self.resize(400, 200)
        self.center()
        self.setWindowTitle("FR:Login")

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)

        self.input_group = QGroupBox("Inputs")
        self.inputs_layout = QVBoxLayout()
        self.inputs_layout.setSpacing(15)

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Login...")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password...")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.inputs_layout.addStretch()
        self.inputs_layout.addWidget(self.login_input)
        self.inputs_layout.addWidget(self.password_input)
        self.inputs_layout.addStretch()

        self.login_btn_layout = QHBoxLayout()
        self.login_btn = QPushButton("Login")
        self.help_btn = QPushButton("⍰️")
        self.login_btn.setStyleSheet("background-color: #a6f299; color: black; border: none;")
        self.login_btn_layout.addStretch()
        self.login_btn.setFixedSize(100, 30)
        self.help_btn.setFixedSize(30, 30)
        self.login_btn_layout.addStretch()
        self.login_btn_layout.addWidget(self.login_btn)
        self.login_btn_layout.addStretch()
        self.login_btn_layout.addWidget(self.help_btn)

        self.inputs_layout.addLayout(self.login_btn_layout)

        self.input_group.setLayout(self.inputs_layout)

        self.main_layout.addWidget(self.input_group)

        self.setLayout(self.main_layout)

        self.login_btn.clicked.connect(self.login)
        self.help_btn.clicked.connect(lambda: self.manager.help("Введите логин и пароль"))

    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().geometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def login(self):
        login_name = self.login_input.text()
        password = self.password_input.text()

        if not login_name or not password:
            QMessageBox.critical(self, "Error", "Login or password is empty")
        elif login_name and password:
            user = login(login_name, password)
            if user:
                Session.current_user = user
                self.manager.switch("main")
            else:
                QMessageBox.critical(self, "Error", "Wrong login or password")

    def update_user(self):
        pass