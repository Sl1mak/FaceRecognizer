from PyQt5.QtWidgets import (
    QWidget,
)

class MainWindow(QWidget):
    def __init__(self, manager):
        super().__init__()
        self.init_UI()
        self.manager = manager

    def init_UI(self):
        pass
