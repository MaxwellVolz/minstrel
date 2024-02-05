import time
import pyautogui
import pydirectinput
from pynput.mouse import Controller, Button


def right_click_pyautogui():
    print("Performing right click using pyautogui...")
    pyautogui.click(button="right")


def right_click_pynput():
    print("Performing right click using pynput...")
    mouse = Controller()
    mouse.click(Button.right, 1)


def press_key_pyautogui():
    print("Pressing 'k' key using pyautogui...")
    pyautogui.press("k")


def press_key_pydirectinput():
    print("Pressing 'K' key using pydirectinput...")
    pydirectinput.press("k")


if __name__ == "__main__":
    time.sleep(3)  # Initial delay to switch to the target window or application

    # Test right-click using pyautogui
    right_click_pyautogui()
    time.sleep(1)  # Wait for 1 second

    # Test right-click using pynput
    right_click_pynput()
    time.sleep(1)  # Wait for 1 second

    # Test pressing 'K' key using pyautogui
    press_key_pyautogui()
    time.sleep(1)  # Wait for 1 second

    # Test pressing 'K' key using pydirectinput
    press_key_pydirectinput()
    time.sleep(1)  # Wait for 1 second

    print("Test completed.")
