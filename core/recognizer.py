import numpy as np

class Recognizer:
    def __init__(self, db_embeddings, threshold=0.6):
        self.db_embeddings = db_embeddings
        self.threshold = threshold

    def cosine_similarity(self, a, b):
        a = np.array(a)
        b = np.array(b)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def recognize(self, embedding):
        best_name = "Unknown"
        best_score = -1

        for name, db_emb in self.db_embeddings.items():
            sim = self.cosine_similarity(embedding, db_emb)

            if sim > best_score:
                best_score = sim
                best_name = name

        if best_score < self.threshold:
            return "Unknown", float(best_score)

        return best_name, float(best_score)