import os
import time
from threading import Thread, Lock
from pynput import keyboard, mouse
import pyautogui
import cv2
import numpy as np

# Configure paths, debounce time, and screenshot dimensions
screenshot_path = "screenshots"
matches_path = "matches"
debounce_time = 3  # seconds
screenshot_width = 520  # adjustable width
screenshot_height = 80  # adjustable height
last_press_time = 0
lock = Lock()

template_path = (
    "screenshots_for_matching/test.png"  # Path to the template image for matching
)

match_dir = "screenshots_for_matching"
drums_din_match = f"{match_dir}/din.png"
drums_allegro_match = f"{match_dir}/allegro.png"
drums_beats_match = f"{match_dir}/beats.png"
drums_rousing_match = f"{match_dir}/rousing.png"
flute_shriek_match = f"{match_dir}/shriek.png"

# Ensure screenshot and matches directories exist
if not os.path.exists(screenshot_path):
    os.makedirs(screenshot_path)
if not os.path.exists(matches_path):
    os.makedirs(matches_path)


def play_drums_din():
    print("Playing Drums: Din of Darkness")


def play_drums_allegro():
    print("Playing Drums: Allegro")


def play_drums_beats():
    print("Playing Drums: Beats of Alacrity")


def play_drums_rousing():
    print("Playing Drums: Rousing Rhythms")


def play_flute_shriek():
    print("Playing Flute: Shriek of Weakness")


def match_template(image_path, template_paths, threshold=0.8):
    img = cv2.imread(image_path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    matched = False

    for template_path in template_paths:
        template = cv2.imread(template_path, 0)
        w, h = template.shape[::-1]

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)

        if np.any(loc[0]):
            for pt in zip(*loc[::-1]):  # Switch columns and rows
                cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)
                match_confidence = res[pt[1]][pt[0]]
                print(f"Match found with confidence: {match_confidence}")

            match_img_path = os.path.join(matches_path, os.path.basename(image_path))
            cv2.imwrite(match_img_path, img)
            matched = True
            break  # Stop searching after the first match

    if matched:
        # Check which template matched and call the associated function
        if template_path == drums_din_match:
            play_drums_din()
        elif template_path == drums_allegro_match:
            play_drums_allegro()
        elif template_path == drums_beats_match:
            play_drums_beats()
        elif template_path == drums_rousing_match:
            play_drums_rousing()
        elif template_path == flute_shriek_match:
            play_flute_shriek()


def take_screenshot():
    screen_width, screen_height = pyautogui.size()
    left = (screen_width - screenshot_width) // 2
    top = (screen_height - screenshot_height) - 250

    start_time = time.time()
    while time.time() - start_time < 1.4:
        img = pyautogui.screenshot(
            region=(left, top, screenshot_width, screenshot_height)
        )
        timestamp = int(time.time() * 1000)  # current time in milliseconds
        img_path = f"{screenshot_path}/{timestamp}.png"
        img.save(img_path)

        # Pass all template paths to match_template
        template_paths = [
            drums_din_match,
            drums_allegro_match,
            drums_beats_match,
            drums_rousing_match,
            flute_shriek_match,
        ]
        if match_template(img_path, template_paths):
            print("Template matched.")
            break  # Exit the loop after finding a match


# mouse handler
def on_click(x, y, button, pressed):
    global last_press_time
    try:
        if button == mouse.Button.right and pressed:
            current_time = time.time()
            if lock.acquire(blocking=False):  # Attempt to acquire lock without blocking
                if current_time - last_press_time > debounce_time:
                    print(f"Right click pressed at position ({x}, {y})")

                    last_press_time = current_time
                    # Start taking screenshots in a non-blocking way
                    Thread(target=take_screenshot).start()
                lock.release()
    except AttributeError:
        pass


# Listener for mouse events
with mouse.Listener(on_click=on_click) as listener:
    listener.join()
