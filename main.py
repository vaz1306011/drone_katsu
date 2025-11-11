from mydrone import MyDrone
from mydrone.core.game_controller import GameController

md = MyDrone()
gc = GameController(md)
gc.start()
