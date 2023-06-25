from engine.game import Game
from pattern.observer import Observer
from ui.controllers import InputController
from world.verb import VerbType


class InputGameObserver(Observer):

    def __init__(self, game: Game):
        self._game = game

    def update(self, controller: InputController) -> None:
        action = controller.action
        if action.verb.type == VerbType.QUIT:
            self._game.running = False
        elif action.verb.type == VerbType.INVENTORY:
            source = self._game.container(action.verb.source)
            destination = self._game.container(action.verb.destination)
            source.remove(action.object)
            destination.add(action.object)
        elif action.verb.type == VerbType.MOVE:
            self._game.protagonist.location = action.object.leads_to
        self._game.latest_action = action

