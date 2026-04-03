from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QGroupBox, QPushButton
)

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_UI()

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
        self.switch = QPushButton("Register")
        self.login_btn.setFixedSize(100, 30)
        self.switch.setFixedSize(100, 30)
        self.login_btn_layout.addWidget(self.login_btn)
        self.login_btn_layout.addWidget(self.switch)
        self.login_btn_layout.addStretch()

        self.inputs_layout.addLayout(self.login_btn_layout)

        self.input_group.setLayout(self.inputs_layout)

        self.main_layout.addWidget(self.input_group)

        self.setLayout(self.main_layout)

        switch = self.switch.clicked.connect(lambda: self.switch_widget(self.register_window))


    def switch_widget(self, widget):
        widget.show()
        self.hide()


    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().geometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())