from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton
)
from PyQt5.QtGui import QPixmap

from app.session import Session
from app.queries import getModels

from core.webcam_pipeline import WebcamPipeline
from core.detectors.facenet_detector import FaceNetDetector
from core.drawer import Drawer

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

        self.camera_label = QLabel(self)
        self.start_btn = QPushButton("Start")
        self.main_layout.addWidget(self.camera_label)
        self.main_layout.addWidget(self.start_btn)
        self.setting_btn = QPushButton("Settings")
        self.main_layout.addWidget(self.setting_btn)
        self.camera_label.hide()

        self.setting_btn.clicked.connect(lambda: self.manager.show("settings"))
        self.camera = None
        self.start_btn.clicked.connect(self.start_process)

        self.setLayout(self.main_layout)

    def update_user(self):
        if Session.current_user:
            if Session.current_user["role"] == "admin":
                self.reg_btn = QPushButton("New user")
                self.main_layout.addWidget(self.reg_btn)
                self.manager.models_list = getModels(Session.current_user["user_id"])
                print(Session.current_user["user_id"])
                print(self.manager.models_list)

    def start_process(self):
        if not self.manager.active_model_path:
            print("Select model first")
            return

        self.detector = FaceNetDetector(self.manager.active_model_path, 0.5)
        self.drawer = Drawer()

        if self.detector and self.drawer:
            if self.camera is None:
                self.camera_label.show()
                self.camera = WebcamPipeline(self.detector, self.drawer)
                self.camera.frame_ready.connect(self.update_frame)
                self.camera.start()
                self.start_btn.setText("Stop")
                self.setting_btn.hide()
                self.reg_btn.hide()
            else:
                self.camera.stop()
                self.camera = None
                self.start_btn.setText("Start")
                self.setting_btn.show()
                self.reg_btn.show()
                self.camera_label.hide()
        

    def update_frame(self, frame):
        pixmap = QPixmap.fromImage(frame)
        self.camera_label.setPixmap(pixmap)

    def closeEvent(self, event):
        if self.camera:
            self.camera.stop()
        event.accept()
