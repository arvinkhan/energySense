import cv2
import numpy as np

class EnergyDetectors:
    def __init__(self):
        self.bg = cv2.createBackgroundSubtractorMOG2()


    def detect_lights(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        brightness = hsv[:, :, 2].mean()
        return brightness > 90
    
    def detect_fan(self, frame):
        roi = frame[0:int(frame.shape[0] * 0.25), :]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        lap = cv2.Laplacian(gray, cv2.CV_64F)
        variance = lap.var()
        return variance > 1000
    
    def detect_projector(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        bright_areas = [c for c in contours if cv2.contourArea(c) > 800]
        return len(bright_areas) > 0
    

    