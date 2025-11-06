from codrone_edu.drone import Drone

from .key_listener import KeyListener, bind


class GameController:
    MOVE_POWER = 30
    ROW_POWER = 30
    UP_DOWN_POWER = 30

    def __init__(self, drone: Drone):
        self.drone = drone
        self.listener = KeyListener(self)
        self.listener.start()

    @bind("w", True)
    def press_w(self):
        print("按下 W")
        self.drone.set_pitch(30)
        self.drone.move()

    @bind("w", False)
    def release_w(self):
        print("放開 W")
        self.drone.set_pitch(0)
        self.drone.move()

    @bind("a", True)
    def press_a(self):
        print("按下 A")
        self.drone.set_roll(-30)
        self.drone.move()

    @bind("a", False)
    def release_a(self):
        print("放開 A")
        self.drone.set_roll(0)
        self.drone.move()

    @bind("s", True)
    def press_s(self):
        print("按下 S")
        self.drone.set_pitch(-30)
        self.drone.move()

    @bind("s", False)
    def release_s(self):
        print("放開 S")
        self.drone.set_pitch(0)
        self.drone.move()

    @bind("d", True)
    def press_d(self):
        print("按下 D")
        self.drone.set_roll(30)
        self.drone.move()

    @bind("d", False)
    def release_d(self):
        print("放開 D")
        self.drone.set_roll(0)
        self.drone.move()

    @bind("h", True)
    def press_h(self):
        print("按下 h")
        self.drone.set_yaw(-30)
        self.drone.move()

    @bind("h", False)
    def release_h(self):
        print("放開 h")
        self.drone.set_yaw(0)
        self.drone.move()

    @bind("j", True)
    def press_j(self):
        print("按下 J")
        self.drone.set_throttle(30)
        self.drone.move()

    @bind("j", False)
    def release_j(self):
        print("放開 J")
        self.drone.set_throttle(0)
        self.drone.move()

    @bind("k", True)
    def press_k(self):
        print("按下 K")
        self.drone.set_throttle(-30)
        self.drone.move()

    @bind("k", False)
    def release_k(self):
        print("放開 K")
        self.drone.set_throttle(0)
        self.drone.move()

    @bind("l", True)
    def press_l(self):
        print("按下 L")
        self.drone.set_yaw(30)
        self.drone.move()

    @bind("l", False)
    def release_l(self):
        print("放開 L")
        self.drone.set_yaw(0)
        self.drone.move()
