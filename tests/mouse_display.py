import pyautogui

screenWidth, screenHeight = pyautogui.size()
print(screenWidth, screenHeight)

currentMouseX, currentMouseY = pyautogui.position()  # Get the XY position of the mouse.
print(currentMouseX, currentMouseY)

pyautogui.alert("After this message a spiral will be drawn.")


def draw_square_spiral(size=100, speed=0.3, tween=pyautogui.easeInOutQuad):

    distance = size

    while distance > 0:
        pyautogui.drag(distance, 0, duration=speed, tween=tween)  # move right
        distance -= 5
        pyautogui.drag(0, distance, duration=speed, tween=tween)  # move down
        pyautogui.drag(-distance, 0, duration=speed, tween=tween)  # move left
        distance -= 5
        pyautogui.drag(0, -distance, duration=speed, tween=tween)  # move up


draw_square_spiral(50, 0.1, pyautogui.easeInQuad)
