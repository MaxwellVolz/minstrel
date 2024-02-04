from pynput import keyboard
import pytest


def test_keyboard_interaction():
    # This test will simply check if the listener can be started and stopped. Lame.
    listener = keyboard.Listener(
        on_press=lambda key: None,
        on_release=lambda key: False if key == keyboard.Key.esc else True,
    )
    listener.start()
    listener.stop()
