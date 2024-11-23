import pyautogui
import threading
import random
import time
import psutil
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw

# Global control variables
stop_event = threading.Event()
last_activity_time = time.time()
idle_time_threshold = 20  # Move mouse after 20 seconds of inactivity

def is_screen_locked():
    """Check if the screen is locked (Windows/Linux)."""
    try:
        if psutil.WINDOWS:
            import win32gui, win32process
            hwnd = win32gui.GetForegroundWindow()
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            return psutil.Process(pid).name().lower() == "logonui.exe"
        elif psutil.LINUX:
            with open("/proc/uptime", "r") as f:
                idle_time = float(f.read().split()[0])
            return idle_time > 300
    except Exception:
        return False

def move_mouse_at_intervals():
    """Move the mouse once every threshold seconds if the user is inactive."""
    while not stop_event.is_set():
        global last_activity_time
        current_time = time.time()

        if current_time - last_activity_time >= idle_time_threshold and not is_screen_locked():
            x, y = pyautogui.position()
            delta_x = random.randint(-10, 10)
            delta_y = random.randint(-10, 10)
            pyautogui.moveTo(x + delta_x, y + delta_y, duration=0.5)
            pyautogui.press('shift')  # Simulate a harmless keypress
            last_activity_time = current_time

        stop_event.wait(0.5)  # Check every 0.5 seconds

def on_mouse_activity(x, y):
    """Update the last activity timestamp when the user moves the mouse."""
    global last_activity_time
    last_activity_time = time.time()

def on_keyboard_activity(key):
    """Update the last activity timestamp when the user uses the keyboard."""
    global last_activity_time
    last_activity_time = time.time()

def stop_program(icon, item):
    """Stop the program."""
    stop_event.set()
    icon.stop()

def create_image():
    """Create a tray icon image."""
    image = Image.new("RGB", (64, 64), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.rectangle((16, 16, 48, 48), fill=(0, 0, 255))
    return image

def setup_tray():
    """Set up the system tray icon."""
    icon_image = create_image()
    menu = Menu(MenuItem("Exit", stop_program))
    icon = Icon("Auto Mouse Mover", icon_image, "Mouse Mover", menu)
    threading.Thread(target=icon.run, daemon=True).start()

if __name__ == "__main__":
    setup_tray()

    # Start mouse listener
    mouse_listener = MouseListener(on_move=on_mouse_activity)
    mouse_listener.start()

    # Start keyboard listener
    keyboard_listener = KeyboardListener(on_press=on_keyboard_activity)
    keyboard_listener.start()

    # Start mouse mover thread
    mover_thread = threading.Thread(target=move_mouse_at_intervals, daemon=True)
    mover_thread.start()

    try:
        while not stop_event.is_set():
            stop_event.wait(10)  # Wait longer to reduce resource consumption
    except KeyboardInterrupt:
        stop_event.set()
    finally:
        mouse_listener.stop()
        keyboard_listener.stop()
