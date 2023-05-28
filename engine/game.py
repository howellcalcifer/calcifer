from calcifer.calcifer import Calcifer
from ui.controller import UIController


class Game:
    def __init__(self, ui: UIController, calcifer: Calcifer):
        self.ui = ui
        self.calcifer = calcifer

    def start(self):
        self.ui.show_scene(self.calcifer.description)
        self.ui.await_user_action()
