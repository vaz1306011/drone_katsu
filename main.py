from mydrone import MyDrone, setup_logging
from mydrone.core.game_controller import GameController

setup_logging()

md = MyDrone()
gc = GameController(md)
gc.start()
