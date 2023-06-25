from engine.action_resolver import ActionResolver
from engine.exceptions import InvalidUnresolvedAction
from engine.game import Game
from pattern.observer import Observer
from ui.controllers import InputController
from world.verb import VerbType


class InputGameObserver(Observer):

    def __init__(self, game: Game):
        self._game = game
        self._action_resolver = ActionResolver(game)

    def update(self, controller: InputController) -> None:
        try:
            action = self._action_resolver.resolve(controller.action)
        except InvalidUnresolvedAction as e:
            self._game.latest_rejected_action = e
            return
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

