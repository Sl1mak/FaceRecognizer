from deepface import DeepFace

class FaceDatabase:
    def __init__(self, model_name="Facenet"):
        self.model_name = model_name
        self.db = {}

    def add_person(self, name, image_path):
        embedding = DeepFace.represent(
            img_path=image_path,
            model_name=self.model_name,
            enforce_detection=False
        )[0]["embedding"]

        self.db[name] = embedding

    def get_all(self):
        return self.db