import os
import time
from threading import Thread, Lock
from pynput import keyboard
import pyautogui
import cv2
import numpy as np

# Configure paths, debounce time, and screenshot dimensions
screenshot_path = "screenshots"
matches_path = "matches"
debounce_time = 2  # seconds
screenshot_width = 200  # adjustable width
screenshot_height = 100  # adjustable height
last_press_time = 0
lock = Lock()

template_path = (
    "screenshots_for_matching/test.png"  # Path to the template image for matching
)

# Ensure screenshot and matches directories exist
if not os.path.exists(screenshot_path):
    os.makedirs(screenshot_path)
if not os.path.exists(matches_path):
    os.makedirs(matches_path)


def match_template(image_path, template_path, threshold=0.8):
    img = cv2.imread(image_path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(template_path, 0)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)

    for pt in zip(*loc[::-1]):  # Switch columns and rows
        cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)
        match_confidence = res[pt[1]][pt[0]]
        print(f"Match found with confidence: {match_confidence}")

    if np.any(loc[0]):
        match_img_path = os.path.join(matches_path, os.path.basename(image_path))
        cv2.imwrite(match_img_path, img)
        return True
    return False


def take_screenshot():
    screen_width, screen_height = pyautogui.size()
    left = (screen_width - screenshot_width) // 2
    top = (screen_height - screenshot_height) - 200

    start_time = time.time()
    while time.time() - start_time < 2:
        img = pyautogui.screenshot(
            region=(left, top, screenshot_width, screenshot_height)
        )
        timestamp = int(time.time() * 1000)  # current time in milliseconds
        img_path = f"{screenshot_path}/{timestamp}.png"
        img.save(img_path)
        if match_template(img_path, template_path):
            print("Template matched.")
            break  # Exit the loop after finding a match


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