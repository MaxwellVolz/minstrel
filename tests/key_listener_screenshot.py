from pynput import keyboard
import pyautogui


def on_press(key):
    try:
        if key.char == "e":  # Check if 'E' is pressed
            # Calculate the rectangle's position
            screen_width, screen_height = pyautogui.size()
            screenshot_width = 200
            screenshot_height = 100

            left = int((screen_width - screenshot_width) / 2)

            top = int(
                (screen_height - 200 - 100)
            )  # 200 pixels from bottom, rectangle height is 100
            # Take and save the screenshot
            screenshot = pyautogui.screenshot(
                region=(left, top, screenshot_width, screenshot_height)
            )
            screenshot.save("screenshot.png")
            print("Screenshot taken.")
    except AttributeError:
        pass  # Ignore non-character keys


# Set up listener for key press
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Keep the script running
listener.join()
