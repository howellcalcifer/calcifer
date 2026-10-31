from engine.action_resolver import ActionResolver
from engine.exceptions import InvalidUnresolvedAction
from engine.events import ActionApplied, ActionRejected, InputEvent, InputRejected
from engine.game import Game
from pattern.observer import Observer
from world.item import Inventory, Item
from world.location import Exit
from world.verb import InventoryVerb, VerbType


class InputGameObserver(Observer[InputEvent]):

    def __init__(self, game: Game):
        self._game = game
        self._action_resolver = ActionResolver(game)

    def update(self, event: InputEvent) -> None:
        if isinstance(event, InputRejected):
            self._game.publish(ActionRejected(event.error))
            return
        try:
            action = self._action_resolver.resolve(event.action)
        except InvalidUnresolvedAction as e:
            self._game.publish(ActionRejected(e))
            return
        if action.verb.type == VerbType.QUIT:
            self._game.stop()
        elif action.verb.type == VerbType.INVENTORY:
            assert isinstance(action.verb, InventoryVerb)
            assert isinstance(action.object, Item)
            source = self._game.container(action.verb.source)
            destination = self._game.container(action.verb.destination)
            assert isinstance(source, Inventory)
            assert isinstance(destination, Inventory)
            source.remove(action.object)
            destination.add(action.object)
        elif action.verb.type == VerbType.MOVE:
            assert isinstance(action.object, Exit)
            assert self._game.protagonist is not None
            self._game.protagonist.location = action.object.leads_to
        self._game.publish(ActionApplied(action))

