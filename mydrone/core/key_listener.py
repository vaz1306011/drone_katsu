import logging

from pynput import keyboard

logger = logging.getLogger(__name__)


def bind(key, is_press: bool):
    """
    裝飾器：綁定按鍵事件到類別方法
    key: "a" or "key.space"
    is_press: True = 按下；False = 放開
    """

    def decorator(func):
        func._key_bind = (key, is_press)  # 標記此方法的綁定資訊
        return func

    return decorator


class KeyListener:
    def __init__(self, owner=None, move_bindings=None):
        self.owner = owner
        self.is_pressing = set()
        self.move_bindings = move_bindings or {}
        self.press_bindings = {}
        self.release_bindings = {}
        self.__collect_bindings(owner)
        self.listener = keyboard.Listener(
            on_press=self.__on_press, on_release=self.__on_release
        )

    def start(self):
        logger.info("KeyListener started")
        self.listener.start()

    def stop(self):
        logger.info("KeyListener stopping")
        self.listener.stop()

    @staticmethod
    def normalize(key):
        if hasattr(key, "char") and key.char:
            return key.char.lower()
        return str(key).lower()

    def __collect_bindings(self, owner):
        for attr_name in dir(owner):
            method = getattr(owner, attr_name)
            if not hasattr(method, "_key_bind"):
                continue

            key, is_press = method._key_bind
            key = self.normalize(key)
            if is_press:
                self.press_bindings[key] = method
            else:
                self.release_bindings[key] = method

    def __on_press(self, key):
        k = self.normalize(key)
        if k in self.is_pressing:
            return

        if k in self.move_bindings:
            func, power, _ = self.move_bindings[k]
            func(power)
        elif k in self.press_bindings:
            self.press_bindings[k]()
            self.is_pressing.add(k)

    def __on_release(self, key):
        k = self.normalize(key)

        if k in self.move_bindings:
            func, _, power = self.move_bindings[k]
            func(power)
        elif k in self.release_bindings:
            self.release_bindings[k]()
            self.is_pressing.discard(k)
