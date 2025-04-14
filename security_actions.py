import os
import platform
import tkinter as tk

def lock_screen():
    system = platform.system()
    if system == "Windows":
        os.system("rundll32.exe user32.dll,LockWorkStation")
    elif system == "Darwin":  # macOS
        os.system("osascript -e 'tell application \"System Events\" to keystroke \"q\" using {control down, command down}'")
    elif system == "Linux":
        os.system("gnome-screensaver-command -l")
    else:
        print("Screen lock not supported on this OS")

def show_blur_overlay_main(root):
    blur_window = tk.Toplevel(root)
    blur_window.overrideredirect(True)
    blur_window.attributes('-fullscreen', True)
    blur_window.attributes('-topmost', True)
    blur_window.configure(bg='black')
    blur_window.attributes('-alpha', 0.7)

    label = tk.Label(blur_window, text="Suspicious Activity Detected", fg="white", bg="black", font=("Helvetica", 24))
    label.pack(expand=True)

    # Auto-close the blur overlay after 5 seconds
    blur_window.after(5000, blur_window.destroy)
