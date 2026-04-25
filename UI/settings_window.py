from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QLineEdit, QLabel, QSizePolicy, QFileDialog,
    QComboBox,
) 

class SettingsWindow(QWidget):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.init_UI()

    def init_UI(self):
        self.resize(300, 100)
        self.setWindowTitle("FR:Settings")
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(10)

        self.model_row = QHBoxLayout()
        self.model_name = QLabel("Model:")
        self.model_name.setFixedWidth(50)

        self.models_list = QComboBox()
        self.models_list.currentTextChanged.connect(self.model_selected)

        self.model_btn = QPushButton("Add")
        self.model_btn.setFixedWidth(40)
        self.model_row.addWidget(self.models_list)
        self.model_row.addWidget(self.model_btn)
        self.main_layout.addLayout(self.model_row)

        self.setLayout(self.main_layout)

        self.model_btn.clicked.connect(lambda: self.manager.show("models"))
    
    def update_user(self):
        self.models_list.clear()
        models = self.manager.getModels()
        for model in models:
            self.models_list.addItem(model[0])

        if models and not self.manager.active_model_name:
            self.manager.setActiveModel(models[0][0])

    def model_selected(self, name):
        self.manager.setActiveModel(name)
