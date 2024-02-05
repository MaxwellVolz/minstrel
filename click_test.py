import time
import pyautogui
from pynput.mouse import Controller, Button
import pydirectinput


def right_click_pyautogui():
    print("Performing right click using pyautogui...")
    pyautogui.click(button="right")


def right_click_pynput():
    print("Performing right click using pynput...")
    mouse = Controller()
    mouse.click(Button.right, 1)


if __name__ == "__main__":
    # Testing pyautogui
    right_click_pyautogui()
    time.sleep(2)  # Wait for 2 seconds

    # Testing pynput
    right_click_pynput()
    time.sleep(1)  # Wait for 2 seconds

    pydirectinput.rightClick()
    pydirectinput.rightClick()
    pydirectinput.rightClick()

    print("Test completed.")
