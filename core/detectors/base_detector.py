class BaseDetector:
    def __init__(self, model_name, threshold=0.5):
        self.model_path = model_name
        self.threshold = threshold

    def detect(self, image):
        raise NotImplementedError("detect() must be implemented")