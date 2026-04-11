from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QLineEdit, QLabel, QSizePolicy, QFileDialog
) 

class SettingsWindow(QWidget):
    def __init__(self, manager):
        super().__init__()
        self.init_UI()
        self.manager = manager

    def init_UI(self):
        self.resize(300, 100)
        self.setWindowTitle("FR:Settings")
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(10)

        self.model_row = QHBoxLayout()
        self.model_name = QLabel("Model:")
        self.model_name.setFixedWidth(50)
        self.model_path = QLineEdit()
        self.model_path.setPlaceholderText("Model path...")
        self.model_path.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.model_path.setReadOnly(True)
        self.model_path.setFixedWidth(300)
        self.model_btn = QPushButton("...")
        self.model_btn.setFixedWidth(40)
        self.model_row.addWidget(self.model_name)
        self.model_row.addWidget(self.model_path)
        self.model_row.addWidget(self.model_btn)
        self.main_layout.addLayout(self.model_row)

        self.setLayout(self.main_layout)

        self.model_btn.clicked.connect(lambda: self.file_dialog(
            self.model_path, 
            title="Choose model", 
            filter="Model files (*.tflite *.oonx *.pt);; All files (*)"
            )
        )
    
    def update_user(self):
        pass

    def file_dialog(self, target_widget, title="Choose file", filter="All files (*)"):
        file_path, _ = QFileDialog.getOpenFileName(self, title, "", filter)
        if file_path:
            target_widget.setText(file_path)
