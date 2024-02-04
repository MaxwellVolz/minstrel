# test_pyautogui_interactions.py
import pytest
import pyautogui


def test_screen_size():
    screenWidth, screenHeight = pyautogui.size()
    assert screenWidth > 0 and screenHeight > 0, "Screen size should be positive"


def test_mouse_position():
    currentMouseX, currentMouseY = pyautogui.position()
    assert (
        currentMouseX >= 0 and currentMouseY >= 0
    ), "Mouse position should be within screen bounds"


def test_draw_spiral():
    # No direct assertion, testing functionality through action
    pyautogui.alert("After this message a spiral will be drawn.")
    draw_square_spiral(50, 0.1, pyautogui.easeInQuad)


def draw_square_spiral(size=100, speed=0.3, tween=pyautogui.easeInOutQuad):
    distance = size
    while distance > 0:
        pyautogui.drag(distance, 0, duration=speed, tween=tween)  # move right
        distance -= 5
        pyautogui.drag(0, distance, duration=speed, tween=tween)  # move down
        pyautogui.drag(-distance, 0, duration=speed, tween=tween)  # move left
        distance -= 5
        pyautogui.drag(0, -distance, duration=speed, tween=tween)  # move up
