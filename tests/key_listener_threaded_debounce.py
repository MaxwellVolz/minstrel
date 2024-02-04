import os
import time
from threading import Thread, Lock
from pynput import keyboard
import pyautogui

# Configure paths, debounce time, and screenshot dimensions
screenshot_path = "screenshots"
debounce_time = 2  # seconds
screenshot_width = 200  # adjustable width
screenshot_height = 100  # adjustable height
last_press_time = 0
lock = Lock()

# Ensure screenshot directory exists
if not os.path.exists(screenshot_path):
    os.makedirs(screenshot_path)


def take_screenshot():
    screen_width, screen_height = pyautogui.size()
    left = (screen_width - screenshot_width) // 2
    top = (
        screen_height - screenshot_height
    ) - 200  # 200 pixels from the bottom, adjust as needed

    start_time = time.time()
    while time.time() - start_time < 2:
        img = pyautogui.screenshot(
            region=(left, top, screenshot_width, screenshot_height)
        )
        timestamp = int(time.time() * 1000)  # current time in milliseconds
        img.save(f"{screenshot_path}/{timestamp}.png")


def on_press(key):
    global last_press_time
    try:
        if key.char == "e":  # Check if 'E' or 'e' is pressed
            current_time = time.time()
            if lock.acquire(blocking=False):  # Attempt to acquire lock without blocking
                if current_time - last_press_time > debounce_time:
                    last_press_time = current_time
                    # Start taking screenshots in a non-blocking way
                    Thread(target=take_screenshot).start()
                lock.release()
    except AttributeError:
        pass


# Listener for keyboard events
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
