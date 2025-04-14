import tkinter as tk
from tkinter import ttk
from threading import Thread
import cv2
from PIL import Image, ImageTk, ImageDraw
from main import run_detection
import time
import pystray
import sys
from queue import Queue, Empty
from utils import alert_user

class ShoulderSurfingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Anti-Shoulder Surfing System")
        self.root.geometry("400x550")
        self.root.resizable(False, False)

        self.protection_enabled = tk.BooleanVar(value=False)
        self.alert_type = tk.StringVar(value="Popup")
        self.alert_delay = tk.IntVar(value=3)
        self.action_mode = tk.StringVar(value="lock")  # New: Lock or Blur

        self.cap = cv2.VideoCapture(0)

        self.build_ui()

        self.thread = None
        self.alert_queue = Queue()
        self.check_alert_queue()
        self.update_video()

        self.root.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)

    def build_ui(self):
        tk.Label(self.root, text="Anti-Shoulder Surfing", font=("Helvetica", 16)).pack(pady=10)

        ttk.Checkbutton(self.root, text="Enable Protection", variable=self.protection_enabled,
                        command=self.toggle_protection).pack(pady=10)

        tk.Label(self.root, text="Alert Type:").pack()
        ttk.Combobox(self.root, textvariable=self.alert_type,
                     values=["Popup", "Sound", "Voice"], state="readonly").pack(pady=5)

        tk.Label(self.root, text="Alert Delay (seconds):").pack()
        ttk.Spinbox(self.root, from_=1, to=10, textvariable=self.alert_delay).pack(pady=5)

        tk.Label(self.root, text="Action on Detection:").pack()
        ttk.Combobox(self.root, textvariable=self.action_mode,
                     values=["lock", "blur"], state="readonly").pack(pady=5)

        self.status_label = tk.Label(self.root, text="Status: OFF", fg="red", font=("Arial", 12))
        self.status_label.pack(pady=10)

        self.video_label = tk.Label(self.root)
        self.video_label.pack(pady=10)

    def toggle_protection(self):
        if self.protection_enabled.get():
            self.status_label.config(text="Status: ON", fg="green")
            self.thread = Thread(target=self.run_detection_thread, daemon=True)
            self.thread.start()
        else:
            self.status_label.config(text="Status: OFF", fg="red")

    def run_detection_thread(self):
        while self.protection_enabled.get():
            alert_needed = run_detection(self.alert_type.get(), self.alert_delay.get(), self.action_mode.get(), self.root)
            if alert_needed:
                self.alert_queue.put(self.alert_type.get())
                time.sleep(self.alert_delay.get())
            time.sleep(1)

    def check_alert_queue(self):
        try:
            while True:
                alert_type = self.alert_queue.get_nowait()
                alert_user(alert_type)  # Safe on main thread
        except Empty:
            pass
        self.root.after(100, self.check_alert_queue)

    def update_video(self):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk)
        self.root.after(10, self.update_video)

    def minimize_to_tray(self):
        self.root.withdraw()
        self.create_tray_icon()

    def create_tray_icon(self):
        icon_image = self.create_image()

        menu = (
            pystray.MenuItem('Show', self.show_window),
            pystray.MenuItem('Quit', self.quit_app)
        )

        self.tray_icon = pystray.Icon("Anti-Shoulder Surfing", icon_image, "Anti-Shoulder Surfing", menu)
        Thread(target=self.tray_icon.run_detached, daemon=True).start()

    def create_image(self, width=64, height=64, color1=(0, 0, 0), color2=(255, 255, 255)):
        image = Image.new('RGB', (width, height), color1)
        dc = ImageDraw.Draw(image)
        dc.rectangle((width // 4, height // 4, width * 3 / 4, height * 3 / 4), fill=color2)
        return image

    def show_window(self, icon, item):
        self.root.after(0, self.root.deiconify)
        icon.stop()

    def quit_app(self, icon, item):
        icon.stop()
        self.on_closing()

    def on_closing(self):
        self.cap.release()
        self.root.destroy()
        sys.exit()

def run_gui():
    root = tk.Tk()
    app = ShoulderSurfingApp(root)
    root.mainloop()