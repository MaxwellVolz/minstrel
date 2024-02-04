import os
from pynput import keyboard
import pyautogui
import time

# Define the directory for saving screenshots
screenshot_dir = "screenshots"
if not os.path.exists(screenshot_dir):
    os.makedirs(screenshot_dir)


def take_screenshots():
    screen_width, screen_height = pyautogui.size()
    # Calculate the region to capture: (left, top, width, height)
    # Center aligned, 200 pixels margin from the bottom

    width = 300
    height = 100

    left = (screen_width - width) // 2
    top = screen_height - 200 - height

    start_time = time.time()
    while time.time() - start_time < 2:  # Take screenshots for 2 seconds
        screenshot = pyautogui.screenshot(region=(left, top, width, height))
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        screenshot.save(f"{screenshot_dir}/screenshot_{timestamp}.png")
        time.sleep(0.01)  # Adjust delay as needed for burst speed


def on_press(key):
    try:
        if key.char == "e":  # Start taking screenshots on 'E' key press
            print("e pressed")
            take_screenshots()
    except AttributeError:
        pass  # Handle special keys here if needed


# Set up listener for key press
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Keep the script running
listener.join()
