import time
import os

import cv2 as cv
import numpy as np
import pyautogui
from pynput import keyboard
import pydirectinput
import msvcrt


DEBUG = True

loop_time = time.time()


def current_milli_time():
    return round(time.time() * 1000)


if DEBUG:
    cwd = os.getcwd()
    test_start_time = current_milli_time()
    current_run_directory = path = os.path.join(cwd, f"test_data\\{test_start_time}")
    os.mkdir(current_run_directory)

screen_width, screen_height = pyautogui.size()

bottom_mid_top_left_search_area = (screen_width * 0.5, screen_height * 0.5)
bottom_mid_bottom_right_search_area = ((screen_width * 0.7), (screen_height * 0.9))
