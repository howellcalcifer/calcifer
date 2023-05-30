from pattern.observer import Topic
from ui.controller import UIController
from world.action import CoreVerbs, UserAction
from world.character import Calcifer


class Game(Topic):

    def __init__(self, ui: UIController, calcifer: Calcifer):
        super().__init__()
        self.ui = ui
        self.calcifer = calcifer
        self._current_action: UserAction | None = None

    def start(self):
        self.ui.show_scene(self.calcifer.description)
        while True:
            action = self.ui.await_user_action()
            self._current_action = action
            self.publish()
            if action.verb.name == CoreVerbs.QUIT.value:
                break

    @property
    def current_action(self):
        return self._current_action

    @property
    def current_location(self):
        return self.calcifer.location
