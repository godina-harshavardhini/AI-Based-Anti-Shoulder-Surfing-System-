import pyttsx3
import pyautogui
import os
from playsound import playsound
from datetime import datetime

def alert_user(alert_type="Popup"):
    if alert_type == "Popup":
        pyautogui.alert("Warning: Possible shoulder surfer detected!")
    elif alert_type == "Sound":
        playsound("alerts/alert.mp3")
    elif alert_type == "Voice":
        engine = pyttsx3.init()
        engine.say("Warning. Someone might be looking at your screen.")
        engine.runAndWait()

def log_event(message, screenshot_path=None):
    os.makedirs("logs", exist_ok=True)
    with open("logs/events.log", "a") as f:
        log_line = f"[{datetime.now()}] {message}"
        if screenshot_path:
            log_line += f" | Screenshot: {screenshot_path}"
        log_line += "\n"
        f.write(log_line)