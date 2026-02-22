import cv2
import threading
import time
from flask import Flask, render_template, jsonify
from detectors import EnergyDetectors
from mediapipe_detector import PeopleDetector
from utils import calculate_waste
import numpy as np
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

VIDEO_SOURCES = [
    "footage-view.webm",
    "footage-view2.webm",
    "footage-view3.webm",
    0
]

detector = EnergyDetectors()
people_detector = PeopleDetector()

rooms = {}
latest_frames = {}
def display_grid():
    while True:
        frames = []

        for i in range(len(VIDEO_SOURCES)):
            room_name = f"Room {i+1}"
            frame = latest_frames.get(room_name)

            if frame is None:
                frame = np.zeros((240, 320, 3), dtype=np.uint8)

            frame = cv2.resize(frame, (400, 300))
            frames.append(frame)

        while len(frames) < 4:
            frames.append(np.zeros_like(frames[0]))


        row1 = np.hstack([frames[0], frames[1]])
        row2 = np.hstack([frames[2], frames[3]])

        grid = np.vstack([row1, row2])

        cv2.imshow("Energy Monitoring - Grid View", grid)

        if cv2.waitKey(1) & 0xFF == 27:
            break


def video_worker(source, room_name):
    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        print(f"Error: Cannot open video {source}")
        rooms[room_name] = {"error": True}
        return


    rooms[room_name] = {
        "lights": "OFF",
        "people": False,
        "waste": 0,
        "status": "ok"
    }

    last_print = time.time() 

    while True:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        
        latest_frames[room_name] = frame

        people_present = people_detector.detect(frame)
        lights_on = detector.detect_lights(frame)

        waste_raw = calculate_waste(["lights"]) if (lights_on and not people_present) else 0
        waste = waste_raw[0] if isinstance(waste_raw, tuple) else waste_raw

        status = (
            "danger" if waste > 30 else
            "warn" if waste > 0 else
            "ok"
        )

        rooms[room_name]["lights"] = "ON" if lights_on else "OFF"
        rooms[room_name]["people"] = bool(people_present)
        rooms[room_name]["waste"] = waste
        rooms[room_name]["status"] = status


        if time.time() - last_print >= 1:
            print(f"[{room_name}] lights={lights_on}  people={people_present}  waste={waste}  status={status}")
            last_print = time.time()

        time.sleep(0.07)

        

def start_video_threads():
    for i, src in enumerate(VIDEO_SOURCES):
        room_name = f"Room {i+1}"
        t = threading.Thread(target=video_worker, args=(src, room_name), daemon=True)
        t.start()

@app.route("/")
def dashboard():
    return render_template("index.html")


@app.route("/live-data")
def live_data():
    return jsonify(rooms)


if __name__ == "__main__":
    start_video_threads()


    flask_thread = threading.Thread(target=lambda: app.run(debug=True, use_reloader=False))
    flask_thread.daemon = True
    flask_thread.start()


    display_grid()