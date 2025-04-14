import cv2
import mediapipe as mp

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

def detect_faces():
    cap = cv2.VideoCapture(0)
    face_boxes = []

    with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.6) as face_detection:
        ret, frame = cap.read()
        if not ret:
            return []

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detection.process(image)

        if results.detections:
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                face_boxes.append((bbox.xmin, bbox.ymin, bbox.width, bbox.height))

    cap.release()
    return face_boxes

