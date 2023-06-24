from engine.game import Game
from pattern.observer import Observer
from ui.controllers import InputController
from world.character import Gesture
from world.scene import Scene
from world.verb import VerbType


class InputGameObserver(Observer):

    def __init__(self, game: Game):
        self._game = game

    def update(self, controller: InputController) -> None:
        action = controller.action
        if action.verb.type == VerbType.QUIT:
            self._game.running = False
        if action.verb.type == VerbType.INVENTORY:
            source = self._game.container(action.verb.source)
            destination = self._game.container(action.verb.destination)
            source.remove(action.object)
            destination.add(action.object)
        if action.verb.type == VerbType.LOOK:
            self._game.protagonist.looking_at = action.object if action.object else self._game.protagonist.location
        if action.verb.type == VerbType.GESTURE:
            self._game.protagonist.gesture = Gesture(name=action.verb.name,
                                                     description=(
                                                         action.verb.description if action.verb.description else
                                                         Scene(f"You {action.verb.name}.")))
