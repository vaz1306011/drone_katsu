import logging

import serial
import serial.serialutil

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
            "w": [self.drone.set_pitch, self.MOVE_POWER, 0],
            "a": [self.drone.set_roll, -self.MOVE_POWER, 0],
            "s": [self.drone.set_pitch, -self.MOVE_POWER, 0],
            "d": [self.drone.set_roll, self.MOVE_POWER, 0],
            "key.space": [self.drone.set_throttle, self.UP_DOWN_POWER, 40],
            "key.shift": [self.drone.set_throttle, -self.UP_DOWN_POWER, 40],
            "j": [self.drone.set_yaw, self.ROW_POWER, 0],
            "k": [self.drone.set_yaw, -self.ROW_POWER, 0],
        }
        self.listener = KeyListener(self, self.bindings)

    def start(self):
        logger.info("GameController started")
        self.listener.start()
        self.drone.start()
        self.is_running = True
        while self.is_running:
            try:
                self.drone.move()
            except serial.serialutil.SerialException:
                break

    def stop(self):
        logger.info("GameController stopping")
        self.drone.stop()
        self.listener.stop()
        self.is_running = False

    @bind("key.esc", True)
    def press_esc(self):
        self.stop()
