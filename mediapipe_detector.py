import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class PeopleDetector:
    def __init__(self):
        BaseOptions = python .BaseOptions
        ObjectDetector = vision.ObjectDetector
        ObjectDetectorOptions = vision.ObjectDetectorOptions
        self.options = ObjectDetectorOptions(
            base_options = BaseOptions(model_asset_path="efficientdet_lite0.tflite"),
            max_results = 5,
            score_threshold = 0.5
        )
        self.detector = ObjectDetector.create_from_options(self.options)

    def detect(self, frame):
        # Convert BGR to RGB
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

        result = self.detector.detect(mp_image)

        # Check if any detected object is a person
        for det in result.detections:
            if det.categories[0].category_name == "person":
                return True

        return False
