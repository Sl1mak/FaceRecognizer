from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QGroupBox, QPushButton
)

class RegisterWindow(QWidget):
    def __init__(self, manager):
        super().__init__()
        self.init_UI()
        self.manager = manager

    def init_UI(self):
        self.resize(400, 200)
        self.center()
        self.setWindowTitle("FR:Register")

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
        self.gmail_input = QLineEdit()
        self.gmail_input.setPlaceholderText("Gmail...")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.inputs_layout.addStretch()
        self.inputs_layout.addWidget(self.login_input)
        self.inputs_layout.addWidget(self.gmail_input)
        self.inputs_layout.addWidget(self.password_input)
        self.inputs_layout.addStretch()

        self.login_btn_layout = QHBoxLayout()
        self.reg_btn = QPushButton("Register")
        self.reg_btn.setStyleSheet("background-color: #a6f299; color: black; border: none;")
        self.login_btn_layout.addStretch()
        self.switch = QPushButton("Login")
        self.switch.setStyleSheet("background-color: skyblue; color: black; border: none;")
        self.reg_btn.setFixedSize(100, 30)
        self.switch.setFixedSize(100, 30)
        self.login_btn_layout.addWidget(self.switch)
        self.login_btn_layout.addWidget(self.reg_btn)
        self.login_btn_layout.addStretch()

        self.inputs_layout.addLayout(self.login_btn_layout)

        self.input_group.setLayout(self.inputs_layout)

        self.main_layout.addWidget(self.input_group)

        self.setLayout(self.main_layout)

        self.reg_btn.clicked.connect(self.register)
        self.switch.clicked.connect(lambda: self.manager.switch("login"))


    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().geometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def register(self):
        login_name = self.login_input.text()
        password = self.password_input.text()
        gmail = self.gmail_input.text()

        if not login_name or not password or not gmail:
            QMessageBox.critical(self, "Error", "Login, gmail or password is empty")
        elif len(password) < 8:
            QMessageBox.critical(self, "Error", "Password is too short")
        else:
            self.manager.switch("main")