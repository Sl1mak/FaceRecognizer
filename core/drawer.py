import cv2 as cv

class Drawer:
    def __init__(self, config=None):
        self.config = config or {
            "font_scale": 0.8,
            "thickness": 2,
            "margin": 5
        }

    def get_color(self, score):
        if score < 0.6:
            return (0, 0, 255)     
        elif score < 0.75:
            return (0, 255, 255)     
        else:
            return (0, 255, 0)       

    def draw(self, image, detections):
        h, w = image.shape[:2]

        for det in detections:
            x, y, bw, bh = det.get("bbox", [0, 0, 0, 0])
            label = det.get("label", "Unknown")
            score = round(det.get("score", 0.0), 2)

            color = self.get_color(score)

            start_point = (int(x), int(y))
            end_point = (int(x + bw), int(y + bh))

            cv.rectangle(
                image,
                start_point,
                end_point,
                color,
                self.config["thickness"]
            )

            text = f"{label} ({score})"

            text_y = y - self.config["margin"]
            if text_y < 10:
                text_y = y + 20

            text_pos = (int(x), int(text_y))

            cv.putText(
                image,
                text,
                text_pos,
                cv.FONT_HERSHEY_COMPLEX,
                self.config["font_scale"],
                color,
                self.config["thickness"]
            )

        return image