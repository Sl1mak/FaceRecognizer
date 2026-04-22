import cv2 as cv

from PyQt5.QtGui import QImage
from PyQt5.QtCore import pyqtSignal, QThread

class WebcamPipeline(QThread):
    frame_ready = pyqtSignal(QImage)

    def __init__(self, camera_index=0):
        super().__init__()
        self.camera_index = camera_index
        self.running = False

    def run(self):
        self.cap = cv.VideoCapture(self.camera_index)
        self.running = True

        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                continue

            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

            h, w, ch = frame.shape
            bytes_per_line = ch * w

            image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888).copy()
            self.frame_ready.emit(image)

        self.cap.release()

    def stop(self):
        self.running = False
        self.quit()
        self.wait()