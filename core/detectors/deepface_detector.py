import cv2 as cv
import numpy as np
from deepface import DeepFace

from core.detectors.base_detector import BaseDetector

class DeepFaceDetector(BaseDetector):
    def __init__(self, model_name="Facenet", threshold=0.7):
        super().__init__(model_name, threshold)

        self.model_name = model_name
        self.threshold = threshold

        import mediapipe as mp
        self.mp_face = mp.solutions.face_detection
        self.face_detector = self.mp_face.FaceDetection(
            model_selection=0,
            min_detection_confidence=0.5
        )

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

                embedding = DeepFace.represent(
                    img_path=face,
                    model_name=self.model_name,
                    enforce_detection=False
                )[0]["embedding"]

                output.append({
                    "bbox": [x, y, bw, bh],
                    "embedding": embedding
                })

        return output


def recognize(embedding, db_embeddings, threshold=0.7):
    best_name = "Unknown"
    best_score = -1

    for name, db_emb in db_embeddings.items():
        score = DeepFace.verify(
            img1_path=np.array(embedding),
            img2_path=np.array(db_emb),
            enforce_detection=False
        )["distance"]

        similarity = 1 - score

        if similarity > best_score:
            best_score = similarity
            best_name = name

    if best_score < threshold:
        return "Unknown", best_score

    return best_name, best_score