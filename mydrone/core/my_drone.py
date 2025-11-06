from codrone_edu.drone import Drone


class MyDrone(Drone):
    POWER = 200

    def __init__(self):
        super().__init__()
        self.pair()

    def start(self):
        self.takeoff()

    def stop(self):
        self.land()
        self.close()

    def go(self, x, y, z):
        while True:
            now_x = self.get_pos_x()
            now_y = self.get_pos_y()
            now_z = self.get_pos_z()
            print(f"Position: ({now_x}, {now_y}, {now_z})")

            diff_x = int(now_x - x)
            diff_y = int(now_y - y)
            diff_z = int(now_z - z)

            if diff_x == 0 and diff_y == 0 and diff_z == 0:
                break

            self.set_roll(-diff_y * self.POWER / 100)
            self.set_pitch(-diff_x * self.POWER / 100)
            self.set_throttle(-diff_z * self.POWER / 100)
            self.move()

    def test(self):
        self.start()

        self.set_pitch(30)
        self.move()
        self.hover(3)

        self.stop()
