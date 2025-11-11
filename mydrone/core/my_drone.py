from codrone_edu.drone import Drone


class MyDrone(Drone):
    def __init__(self):
        super().__init__()
        self.pair()

    def start(self):
        self.takeoff()

    def stop(self):
        self.land()
        self.close()
