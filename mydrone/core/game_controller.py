import logging

from mydrone import MyDrone

from .key_listener import KeyListener, bind

logger = logging.getLogger(__name__)


class GameController:
    MOVE_POWER = 100
    ROW_POWER = 100
    UP_DOWN_POWER = 100

    def __init__(self, drone: MyDrone):
        self.is_running = True
        self.drone = drone
        self.bindings = {
            "w": [self.drone.set_pitch, self.MOVE_POWER],
            "a": [self.drone.set_roll, -self.MOVE_POWER],
            "s": [self.drone.set_pitch, -self.MOVE_POWER],
            "d": [self.drone.set_roll, self.MOVE_POWER],
            "key.space": [self.drone.set_throttle, self.UP_DOWN_POWER],
            "key.shift": [self.drone.set_throttle, -self.UP_DOWN_POWER],
            "j": [self.drone.set_yaw, self.ROW_POWER],
            "k": [self.drone.set_yaw, -self.ROW_POWER],
        }
        self.listener = KeyListener(self, self.bindings)

    def start(self):
        logger.info("GameController started")
        self.listener.start()
        self.drone.start()
        self.is_running = True
        while self.is_running:
            self.drone.move()

    def stop(self):
        logger.info("GameController stopping")
        self.drone.stop()
        self.listener.stop()
        self.is_running = False

    @bind("key.esc", True)
    def press_esc(self):
        self.stop()
