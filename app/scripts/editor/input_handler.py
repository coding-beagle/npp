from pynput import keyboard


class InputHandler:
    def __init__(self):
        self.listener = keyboard.Listener(
            on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

        self.currently_pressed_keys = []

    def on_press(self, key):
        if (key not in self.currently_pressed_keys):
            self.currently_pressed_keys.append(key)

    def on_release(self, key):
        for i, k in enumerate(self.currently_pressed_keys):
            if k == key:
                self.currently_pressed_keys.pop(i)

    def stop(self):
        self.listener.stop()

    def get_currently_pressed_keys(self):
        return self.currently_pressed_keys
