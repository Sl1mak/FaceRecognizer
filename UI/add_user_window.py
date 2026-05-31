from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QFileDialog, QMessageBox, QHBoxLayout

from app.queries import addUser

class AddUserWindow(QWidget):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.init_UI()

    def init_UI(self):
        self.resize(400, 200)
        self.setWindowTitle("FR:AddUser")

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)

        self.name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.password_input = QLineEdit()
        self.media_path = QLineEdit()
        self.media_file_btn = QPushButton("...")
        self.submit_btn = QPushButton("Submit")

        self.name_input.setPlaceholderText("Name...")
        self.email_input.setPlaceholderText("Email...")
        self.password_input.setPlaceholderText("Password...")
        self.media_path.setPlaceholderText("Image path...")

        self.help_btn = QPushButton("⍰️")
        self.help_btn.setFixedSize(30, 30)
        self.help_btn.clicked.connect(lambda: self.manager.help("Это окно доступно только администратору. Введите все данные в поля и загрузите изображение лица для вненсения его в базу данных. Нажмите кнопку Submit."))

        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.addStretch()
        self.bottom_layout.addWidget(self.help_btn)

        self.password_input.setEchoMode(QLineEdit.Password)

        self.media_file_btn.clicked.connect(lambda: self.file_dialog(self.media_path, "Choose media file", "All files (*)"))
        self.submit_btn.clicked.connect(lambda: self.submit())

        self.main_layout.addWidget(self.name_input)
        self.main_layout.addWidget(self.email_input)
        self.main_layout.addWidget(self.password_input)

        self.main_layout.addWidget(self.media_path)
        self.main_layout.addWidget(self.media_file_btn)
        self.main_layout.addWidget(self.submit_btn)
        self.main_layout.addLayout(self.bottom_layout)

        self.setLayout(self.main_layout)

    def file_dialog(self, target_widget, title="Choose file", filter="All files (*)"):
        file_path, _ = QFileDialog.getOpenFileName(self, title, "", filter)
        if file_path:
            target_widget.setText(file_path)

    def submit(self):
        name_input = self.name_input.text()
        email_input = self.email_input.text()
        password_input = self.password_input.text()
        media_path = self.media_path.text()
        if not all([name_input, email_input, password_input, media_path]):
            QMessageBox.critical(self, "Error", "Name, email, password or media path is empty")
        elif len(password_input) < 8:
            QMessageBox.critical(self, "Error", "Password is too short")
        else:
            try:
                addUser(name_input, email_input, password_input, media_path)
                QMessageBox.information(self, "Success", "User added successfully")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
            except Exception as e:
                QMessageBox.critical(self, "Unexpected Error", str(e))

    def update_user(self):
        pass