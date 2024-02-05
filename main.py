import cv2
import numpy as np
import pyautogui
from pynput import mouse
from pynput.mouse import Button, Listener
import time
import os

# Assuming debounce is correctly implemented in utils.py
from utils import debounce

image_paths = [
    "needles/din.png",
    "needles/beats.png",
    "needles/shriek.png",
    "needles/rousing.png",
    "needles/allegro.png",
]
screenshot_dir = "screenshots"
if not os.path.exists(screenshot_dir):
    os.makedirs(screenshot_dir)


# Function to capture a part of the screen
def capture_screen(region=None, save_path=None):
    screenshot = pyautogui.screenshot(region=region)
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    if save_path:
        if not os.path.exists(os.path.dirname(save_path)):
            os.makedirs(os.path.dirname(save_path))
        cv2.imwrite(save_path, frame)
    return frame


# Function to compare the captured screen with a predefined image
def match_image(captured_frame, image_path, threshold=0.8):
    template = cv2.imread(image_path, 0)
    captured_gray = cv2.cvtColor(captured_frame, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(captured_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    return any(loc[0])  # Returns True if a match is found


@debounce(3)
def check_images(region=None, retries=5, delay=1):
    time.sleep(0.5)  # Initial wait before starting the checks

    for attempt in range(retries):
        captured_frame = capture_screen(region)
        # Save the captured frame with a unique name based on the current timestamp and attempt number
        img_path = (
            f"{screenshot_dir}/screenshot_{int(time.time() * 1000)}_{attempt}.png"
        )
        cv2.imwrite(img_path, captured_frame)

        for image_path in image_paths:
            if match_image(captured_frame, image_path):
                print(f"Match found for {image_path}")
                # Return the path of the matched image for further processing
                return image_path

        time.sleep(delay)  # Wait before the next attempt

    print("No match found after retries.")
    return None  # Indicate no match was found


def execute_procedure_for_image(image_path):
    # Example procedure mapping
    procedures = {
        "needles/din.png": lambda: print("Executing procedure for Din"),
        "needles/beats.png": lambda: print("Executing procedure for Beats"),
        "needles/shriek.png": lambda: print("Executing procedure for Shriek"),
        "needles/rousing.png": lambda: print("Executing procedure for Rousing"),
        "needles/allegro.png": lambda: print("Executing procedure for Allegro"),
    }

    # Get the procedure based on the matched image and execute it
    procedure = procedures.get(image_path)
    if procedure:
        procedure()
    else:
        print("No specific procedure for the matched image.")


def on_click(x, y, button, pressed):
    if button == Button.right and pressed:
        region = (1700, 1120, 30, 5)  # Define the specific region to capture
        matched_image = check_images(
            region=region, retries=5, delay=1
        )  # Adjust retries and delay as needed

        if matched_image:
            print(f"Match found for {matched_image}, proceeding with further actions.")
            execute_procedure_for_image(matched_image)
        else:
            print("No match found, no further actions taken.")


# Start listening for mouse events
with Listener(on_click=on_click) as listener:
    listener.join()
