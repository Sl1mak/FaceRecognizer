from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class HelpWindow(QWidget):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.init_UI()

    def init_UI(self):
        self.resize(200, 100)
        self.setWindowTitle("FR:Help")

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.text = QLabel()

        self.main_layout.addWidget(self.text)
        self.setLayout(self.main_layout)

    def update_user(self):
        pass
