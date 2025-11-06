from pynput import keyboard


def bind(key, is_press: bool):
    """
    裝飾器：綁定按鍵事件到類別方法
    key: "a" or "Key.space"
    is_press: True = 按下；False = 放開
    """

    def decorator(func):
        func._key_bind = (key, is_press)  # 標記此方法的綁定資訊
        return func

    return decorator


class KeyListener:
    def __init__(self, owner=None):
        self.owner = owner
        self.press_bindings = {}  # key → method
        self.release_bindings = {}  # key → method

        self._collect_bindings(owner)

        self.listener = keyboard.Listener(
            on_press=self.__on_press, on_release=self.__on_release
        )

    def _collect_bindings(self, owner):
        """自動讀取類方法上面的 @bind 設定"""
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

    @staticmethod
    def normalize(key):
        """把按鍵統一成一致字串方便比對"""
        if hasattr(key, "char") and key.char:
            return key.char.lower()
        return str(key)

    def __on_press(self, key):
        k = self.normalize(key)
        if k in self.press_bindings:
            self.press_bindings[k]()

    def __on_release(self, key):
        k = self.normalize(key)
        if k in self.release_bindings:
            self.release_bindings[k]()

    def start(self):
        """背景 thread 啟動鍵盤監聽"""
        self.listener.start()

    def stop(self):
        self.listener.stop()
