from functools import partial

from pynput import keyboard


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
        self._collect_bindings(owner)
        self.listener = keyboard.Listener(
            on_press=self.__on_press, on_release=self.__on_release
        )

    def start(self):
        """背景 thread 啟動鍵盤監聽"""
        self.listener.start()

    def stop(self):
        self.listener.stop()

    @staticmethod
    def normalize(key):
        """把按鍵統一成一致字串方便比對"""
        if hasattr(key, "char") and key.char:
            return key.char.lower()
        return str(key).lower()

    def _bind_key(self, key, is_press, method):
        key = key.lower()
        if is_press:
            self.press_bindings[key] = method
        else:
            self.release_bindings[key] = method

    def _collect_bindings(self, owner):
        for attr_name in dir(owner):
            method = getattr(owner, attr_name)
            if hasattr(method, "_key_bind"):
                key, is_press = method._key_bind

                # 正規化 key（避免大小寫差異）
                key = key.lower()

                if is_press:
                    self.press_bindings[key] = method
                else:
                    self.release_bindings[key] = method

    def __on_press(self, key):
        k = self.normalize(key)
        if k in self.is_pressing or k not in self.press_bindings:
            return
        if k in self.move_bindings:
            func, power = self.move_bindings[k]
            func(power)
        self.press_bindings[k]()
        self.is_pressing.add(k)

    def __on_release(self, key):
        k = self.normalize(key)
        if k not in self.release_bindings:
            return
        if k in self.move_bindings:
            func, _ = self.move_bindings[k]
            func(0)
        self.release_bindings[k]()
        self.is_pressing.discard(k)
