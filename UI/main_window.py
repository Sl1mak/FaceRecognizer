from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap

from app.session import Session

from core.webcam_pipeline import WebcamPipeline
from core.detectors.deepface_detector import DeepFaceDetector
from core.drawer import Drawer


class MainWindow(QWidget):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.camera = None
        self.reg_btn = None
        self.init_UI()

    def init_UI(self):
        self.resize(400, 300)
        self.setWindowTitle("FR:Main")

        self.main_layout = QVBoxLayout()

        self.camera_label = QLabel(self)

        self.start_btn = QPushButton("Start")
        self.setting_btn = QPushButton("Settings")

        self.main_layout.addWidget(self.camera_label)
        self.main_layout.addWidget(self.start_btn)
        self.main_layout.addWidget(self.setting_btn)

        self.camera_label.hide()

        self.setting_btn.clicked.connect(lambda: self.manager.show("settings"))
        self.start_btn.clicked.connect(self.start_process)

        self.setLayout(self.main_layout)

    def update_user(self):
        if Session.current_user and Session.current_user["role"] == "admin":
            if not self.reg_btn:
                self.reg_btn = QPushButton("New user")
                self.main_layout.addWidget(self.reg_btn)

    def start_process(self):
        if not self.manager.active_model_name:
            print("Select model first")
            return

        detector = DeepFaceDetector(self.manager.active_model_name, 0.5)
        drawer = Drawer()

        if self.camera is None:
            self.camera_label.show()

            self.camera = WebcamPipeline(detector, drawer)
            self.camera.frame_ready.connect(self.update_frame)
            self.camera.start()

            self.start_btn.setText("Stop")
            self.setting_btn.hide()
            if self.reg_btn:
                self.reg_btn.hide()

        else:
            self.camera.stop()
            self.camera = None

            self.start_btn.setText("Start")
            self.setting_btn.show()
            if self.reg_btn:
                self.reg_btn.show()

            self.camera_label.hide()

    def update_frame(self, frame):
        pixmap = QPixmap.fromImage(frame)
        self.camera_label.setPixmap(pixmap)

    def closeEvent(self, event):
        if self.camera:
            self.camera.stop()
        event.accept()