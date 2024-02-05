import cv2
import numpy as np
import pyautogui
from pynput import mouse, keyboard
import time
from datetime import datetime, timedelta
import pygetwindow as gw
import time
from pynput.mouse import Controller, Button
import pydirectinput


window_title = "Dark and Darker"
win = gw.getWindowsWithTitle(window_title)[0]  # Get the window with the specific title

if win:
    win.activate()  # Try to bring the window to the front
    time.sleep(1)

toggle = False  # Toggle functionality on/off
right_click_detected = False
watch_areas = []  # Store watch areas


def on_press(key):
    global toggle
    try:
        if key.char == "f":  # Toggle functionality
            toggle = not toggle
            print(f"Functionality toggled {'on' if toggle else 'off'}")
            if toggle:
                global watch_areas  # Reset watch areas when toggled on
                watch_areas = []
    except AttributeError:
        pass


def on_click(x, y, button, pressed):
    global right_click_detected
    if button == mouse.Button.right and pressed and toggle:
        right_click_detected = True  # Set the flag when right click is detected


def capture_area(area):
    """Capture the screen region defined by area."""
    x, y, w, h = area
    capture = pyautogui.screenshot(region=(x, y, w, h))
    capture_np = np.array(capture)
    return cv2.cvtColor(capture_np, cv2.COLOR_BGR2RGB)


def compare_images(img1, img2, threshold=30):
    """Compare two images and return True if they are different beyond a threshold."""
    diff = cv2.absdiff(img1, img2)
    non_zero_count = np.count_nonzero(diff)
    print(non_zero_count)
    return non_zero_count > threshold


def process_screen():
    global watch_areas
    watch_areas = []
    screen = pyautogui.screenshot(region=(1500, 1150, 480, 26))
    screen_np = np.array(screen)
    screen_np = cv2.cvtColor(screen_np, cv2.COLOR_BGR2RGB)
    lower = np.array([5, 170, 230])
    upper = np.array([30, 200, 255])
    mask = cv2.inRange(screen_np, lower, upper)
    kernel = np.ones((5, 5), np.uint8)

    mask_processed = cv2.dilate(mask, kernel, iterations=1)
    mask_processed = cv2.erode(mask_processed, kernel, iterations=1)

    contours, _ = cv2.findContours(
        mask_processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    if not contours:
        print("No areas to monitor.")
        return False  # Signal to exit monitoring

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        watch_x = x - 18  # Position the watch area
        watch_y = y + (h // 2) - 3
        watch_areas.append((watch_x, watch_y, 7, 7))  # Store area

        cv2.rectangle(screen_np, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.rectangle(
            screen_np,
            (watch_x, watch_y),
            (watch_x + 6, watch_y + 6),
            (255, 255, 0),
            2,
        )

    cv2.imwrite(
        "screen_with_rectangles.png", cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)
    )

    return True  # Signal that areas were found and watch_areas is populated


def capture_initial_states():
    return [capture_area(area) for area in watch_areas]


def monitor_watch_area(area, initial_img, duration=3, n=0):
    mouse = Controller()

    start_time = datetime.now()
    while (datetime.now() - start_time).seconds < duration:
        current_img = capture_area(area)
        if compare_images(initial_img, current_img):
            print("Significant change detected.")
            # pyautogui.click(button="right")  # Simulate right mouse click+
            # mouse.click(Button.right, 1)
            pydirectinput.press("k")
            time.sleep(0.05)
            return True  # Return immediately upon detecting a significant change
    print("Timed out...")
    return False  # Return False if no significant change is detected


def process_monitoring():
    if process_screen():  # Check and define watch areas
        initial_states = (
            capture_initial_states()
        )  # Capture initial states of all defined watch areas
        for i, area in enumerate(watch_areas):
            monitor_watch_area(area, initial_states[i], 2, i)
            print(f"Beat {i}")


def main():
    global right_click_detected
    keyboard_listener = keyboard.Listener(on_press=on_press)
    mouse_listener = mouse.Listener(on_click=on_click)
    keyboard_listener.start()
    mouse_listener.start()

    try:
        while True:
            if toggle and right_click_detected:
                process_monitoring()  # Start capturing and monitoring on right clickf
                right_click_detected = False  # Reset the flag after processing
            time.sleep(1)  # Adjust as needed for responsiveness vs performance
    except KeyboardInterrupt:
        print("Program terminated by user.")


if __name__ == "__main__":
    main()
