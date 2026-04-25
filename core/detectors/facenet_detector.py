import cv2 as cv
import numpy as np
import mediapipe as mp
import tensorflow as tf

from core.detectors.base_detector import BaseDetector

class FaceNetDetector(BaseDetector):
    def __init__(self, model_path, threshold=0.7):
        super().__init__(model_path, threshold)

        # Face detector (MediaPipe)
        self.mp_face = mp.solutions.face_detection
        self.face_detector = self.mp_face.FaceDetection(model_selection=0, min_detection_confidence=0.5)

        # TFLite interpreter
        self.interpreter = tf.lite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()

        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        self.input_size = self.input_details[0]["shape"][1:3]  # (h, w)

    def _preprocess(self, face):
        face = cv.resize(face, (self.input_size[1], self.input_size[0]))
        face = face.astype(np.float32) / 255.0
        face = np.expand_dims(face, axis=0)
        return face

    def _get_embedding(self, face):
        input_data = self._preprocess(face)
        self.interpreter.set_tensor(self.input_details[0]["index"], input_data)
        self.interpreter.invoke()
        embedding = self.interpreter.get_tensor(self.output_details[0]["index"])[0]
        return embedding

    def detect(self, image):
        h, w, _ = image.shape
        rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)

        results = self.face_detector.process(rgb)

        output = []

        if results.detections:
            for det in results.detections:
                bboxC = det.location_data.relative_bounding_box

                x = int(bboxC.xmin * w)
                y = int(bboxC.ymin * h)
                bw = int(bboxC.width * w)
                bh = int(bboxC.height * h)

                x = max(0, x)
                y = max(0, y)
                bw = min(w - x, bw)
                bh = min(h - y, bh)

                face = image[y:y+bh, x:x+bw]
                if face.size == 0:
                    continue

                embedding = self._get_embedding(face)

                output.append({
                    "bbox": [x, y, bw, bh],
                    "embedding": embedding
                })

        return output

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def recognize(embedding, db_embeddings, threshold=0.7):
    best_name = "Unknown"
    best_score = -1

    for name, db_emb in db_embeddings.items():
        score = cosine_similarity(embedding, db_emb)
        if score > best_score:
            best_score = score
            best_name = name

    if best_score < threshold:
        return "Unknown", best_score

    return best_name, best_score