from world.character import Calcifer
from ui.controller import UIController
from world.action import CoreVerbs
from world.location import Location


class Game:

    def __init__(self, ui: UIController, calcifer: Calcifer):
        self.ui = ui
        self.calcifer = calcifer

    def start(self):
        self.ui.show_scene(self.calcifer.description)
        action = self.ui.await_user_action()
        if action.verb.name == CoreVerbs.LOOK.value:
            self.ui.show_scene(self.calcifer.location.scene)
