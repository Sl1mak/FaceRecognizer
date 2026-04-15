from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit, QFileDialog, QHBoxLayout, 
    QMessageBox
)

from app.queries import addModel
from app.session import Session

class ModelsWindow(QWidget):
    def __init__(self, manager):
        super().__init__()
        self.init_UI()
        self.manager = manager

    def init_UI(self):
        self.resize(400, 200)
        self.setWindowTitle("FR:Models")

        self.model_name = QLineEdit()
        self.model_name.setPlaceholderText("Model name...")
        self.model_path = QLineEdit()
        self.model_file_btn = QPushButton("...")
        self.confirm_button = QPushButton("Confirm")

        self.model_file_btn.clicked.connect(lambda: self.file_dialog(
            self.model_path,
            title="Choose model file",
            filter="Model files (*.tflite *.oonx *.pt);; All files (*)"
            )
        )
        self.confirm_button.clicked.connect(self.confirm_model)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.model_name)
        self.main_layout.addWidget(self.model_path)
        self.main_layout.addWidget(self.model_file_btn)
        self.main_layout.addWidget(self.confirm_button)

        self.setLayout(self.main_layout)

    def file_dialog(self, target_widget, title="Choose file", filter="All files (*)"):
        file_path, _ = QFileDialog.getOpenFileName(self, title, "", filter)
        if file_path:
            target_widget.setText(file_path)

    def confirm_model(self):
        model_name = self.model_name.text()
        model_path = self.model_path.text()
        if model_name and model_path:
            addModel(model_name, model_path, Session.current_user["user_id"])
            self.hide()
        else:
            QMessageBox.critical(self, "Error", "Model name or path is empty")

    def update_user(self):
        pass