from engine.action import UnresolvedAction, UserAction
from engine.container_factory import CurrentContainerType
from engine.exceptions import InvalidUnresolvedAction
from engine.game import Game
from world.character import Character
from world.item import Item
from world.location import Exit
from world.verb import InventoryVerb
from world.verb import VerbType


class ActionResolver:

    def __init__(self, game: Game):
        self.game = game

    def resolve(self, action: UnresolvedAction) -> UserAction:

        if action.object_ref_1 is None:
            if action.verb.type == VerbType.INVENTORY:
                protagonist = self.game.protagonist
                if protagonist is None:
                    raise InvalidUnresolvedAction("There is no active protagonist.")
                return UserAction(verb=action.verb, inventory=tuple(protagonist.inventory.values()))
            if action.verb.type != VerbType.LOOK:
                return UserAction(verb=action.verb)
            protagonist = self.game.protagonist
            if protagonist is None:
                raise InvalidUnresolvedAction("There is no active protagonist.")
            return UserAction(verb=action.verb, object=protagonist.location)

        visible_objects = self.game.container(CurrentContainerType.VISIBLE)
        try:
            obj = visible_objects[action.object_ref_1]
        except KeyError:
            if action.verb.type == VerbType.MOVE:
                raise InvalidUnresolvedAction("You can't go that way.") from None
            else:
                raise InvalidUnresolvedAction(f"You can't see any {action.object_ref_1}.") from None

        if action.verb.type == VerbType.ITEM_TRANSFER:
            if not isinstance(action.verb, InventoryVerb) or not isinstance(obj, (Item, Character)):
                raise InvalidUnresolvedAction(f"You can't {action.verb.name} that.") from None
            source = self.game.container(action.verb.source)
            destination = self.game.container(action.verb.destination)
            if obj.name not in source or obj.name in destination:
                raise InvalidUnresolvedAction(f"You can't {action.verb.name} that.") from None
        if action.verb.type == VerbType.MOVE:
            if not isinstance(obj, Exit):
                raise InvalidUnresolvedAction("You can't go there.") from None
            if obj.direction not in self.game.container(CurrentContainerType.LOCATION_EXITS):
                raise InvalidUnresolvedAction(f"You can't go {obj.direction}")

        return UserAction(verb=action.verb, object=obj)
