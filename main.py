from utils import log_event
from detector import detect_faces
from datetime import datetime
import face_recognition
import cv2
import os
import time
import pickle
from security_actions import lock_screen, show_blur_overlay_main


# Load trusted face encodings once
try:
    with open("known_faces_encodings.pkl", "rb") as f:
        trusted_encodings = pickle.load(f)  # List of tuples: (filename, encoding)
except FileNotFoundError:
    trusted_encodings = []

def run_detection(alert_type, alert_delay, action_mode, root=None):
    faces = detect_faces()
    if len(faces) > 1:
        face_sizes = [w * h for (_, _, w, h) in faces]
        largest = max(face_sizes)
        others = [size for size in face_sizes if size < 0.9 * largest]

        if others:
            screenshot_path = save_screenshot()
            log_event("Suspicious face detected.", screenshot_path)

            if action_mode == "Lock":
                lock_screen()
            elif action_mode == "Blur" and root:
                from security_actions import show_blur_overlay_main
                root.after(0, lambda: show_blur_overlay_main(root))

            return True
    return False



def save_screenshot(frame=None):
    os.makedirs("logs/screenshots", exist_ok=True)

    if frame is None:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        if not ret:
            return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"logs/screenshots/screenshot_{timestamp}.png"
    cv2.imwrite(filename, frame)
    return filename
