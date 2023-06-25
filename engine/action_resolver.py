from engine.action import UnresolvedAction, UserAction
from engine.container_factory import CurrentContainerType
from engine.exceptions import InvalidUnresolvedAction
from engine.game import Game
from world.verb import VerbType


class ActionResolver:

    def __init__(self, game: Game):
        self.game = game

    def resolve(self, action: UnresolvedAction) -> UserAction:

        if action.object_ref_1 is None:
            if action.verb.type != VerbType.LOOK:
                return UserAction(verb=action.verb)
            else:
                return UserAction(verb=action.verb, object=self.game.protagonist.location)

        visible_objects = self.game.container(CurrentContainerType.VISIBLE)
        try:
            obj = visible_objects[action.object_ref_1]
        except KeyError:
            if action.verb.type == VerbType.MOVE:
                raise InvalidUnresolvedAction(f"You can't go that way.")
            else:
                raise InvalidUnresolvedAction(f"You can't see any {action.object_ref_1}.")

        if action.verb.type == VerbType.INVENTORY:
            source = self.game.container(action.verb.source)
            destination = self.game.container(action.verb.destination)
            try:
                if obj.name not in source or obj.name in destination:
                    raise InvalidUnresolvedAction(f"You can't {action.verb.name} that.")
            except AttributeError:
                raise InvalidUnresolvedAction(f"You can't {action.verb.name} that.")
        if action.verb.type == VerbType.MOVE:
            try:
                if obj.direction not in self.game.container(CurrentContainerType.LOCATION_EXITS):
                    raise InvalidUnresolvedAction(f"You can't go {obj.direction}")
            except AttributeError:
                raise InvalidUnresolvedAction("You can't go there.")

        return UserAction(verb=action.verb, object=obj)
