import time


def debounce(wait):
    """Decorator that will postpone a function's
    execution until after `wait` seconds have elapsed since the last time it was invoked.
    """

    def decorator(fn):
        last_call = 0

        def debounced(*args, **kwargs):
            nonlocal last_call
            current_call = time.time()
            if current_call - last_call >= wait:
                last_call = current_call
                return fn(*args, **kwargs)

        return debounced

    return decorator
