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

# Play Bar
screenshot_width = 520  # adjustable width
screenshot_height = 80  # adjustable height

# Song Detection
screenshot_width = 60  # adjustable width
screenshot_height = 20  # adjustable height

screenshot_unlock = True
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

drums_din1_match = f"{match_dir}/din1.png"
drums_allegro1_match = f"{match_dir}/allegro1.png"
drums_beats1_match = f"{match_dir}/beats1.png"
drums_rousing1_match = f"{match_dir}/rousing1.png"

all_drums = [
    drums_din_match,
    drums_allegro_match,
    drums_beats_match,
    drums_rousing_match,
]
# Ensure screenshot and matches directories exist
if not os.path.exists(screenshot_path):
    os.makedirs(screenshot_path)
if not os.path.exists(matches_path):
    os.makedirs(matches_path)


def play_drums_din():
    print("Playing Drums: Din of Darkness")
    # TODO:
    # start checking for first note and
    # if match trigger mouse-rightclick

    if take_screenshot([drums_din1_match], 80, 40, 320, 2):
        pyautogui.click(button="right")


def play_drums_allegro():
    print("Playing Drums: Allegro")

    if take_screenshot([drums_allegro1_match], 80, 40, 320, 2):
        pyautogui.click(button="right")


def play_drums_beats():
    print("Playing Drums: Beats of Alacrity")

    if take_screenshot([drums_beats1_match], 80, 40, 320, 2):
        pyautogui.click(button="right")


def play_drums_rousing():
    print("Playing Drums: Rousing Rhythms")

    if take_screenshot([drums_rousing1_match], 80, 40, 320, 2):
        pyautogui.click(button="right")


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


def take_screenshot(
    template_paths, width=200, height=200, bottom_offset=250, threshold=0.8, duration=3
):
    global should_continue_screenshots
    screen_width, screen_height = pyautogui.size()
    left = (screen_width - width) // 2
    top = screen_height - bottom_offset

    # TODO: if a match is found we should stop taking screenshots

    start_time = time.time()
    while time.time() - start_time < 3:
        img = pyautogui.screenshot(region=(left, top, width, height))
        timestamp = int(time.time() * 1000)  # current time in milliseconds
        img_path = f"{screenshot_path}/{timestamp}.png"
        img.save(img_path)

        if len(template_paths) > 0:
            if match_template(img_path, template_paths, threshold):
                print("Template matched.")
                should_continue_screenshots = False
                return True
                break

    return False


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
                    Thread(
                        target=take_screenshot, args=([*all_drums], 80, 40, 320, 2)
                    ).start()
                lock.release()
    except AttributeError:
        pass


# Listener for mouse events
with mouse.Listener(on_click=on_click) as listener:
    listener.join()
