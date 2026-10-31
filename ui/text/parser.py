from engine.action import UnresolvedAction
from world.location import Direction
from world.mappings import VerbMapping
from world.verb import VerbType


class InvalidUserActionException(Exception):
    pass


class TextParser:
    def __init__(self, verbs: VerbMapping):
        self.verbs = verbs

    def parse_user_action(self, text: str) -> UnresolvedAction:
        words = text.split()
        direction_action = self.parse_direction(words)
        if direction_action is not None:
            return direction_action
        verb = self.parse_verb(words)
        obj = self.parse_object(words, verb)
        return UnresolvedAction(verb=verb, object_ref_1=obj)

    def parse_direction(self, words: list[str]) -> UnresolvedAction | None:
        if len(words) != 1:
            return None

        direction_input = words[0].lower()
        direction = Direction.from_shortcut(direction_input) or Direction.from_name(direction_input)
        if direction is None:
            return None

        move_verb = next(
            (verb for verb in self.verbs.values() if verb.type == VerbType.MOVE),
            None,
        )
        if move_verb is None:
            return None

        return UnresolvedAction(
            verb=move_verb,
            object_ref_1=direction.value,
        )

    @staticmethod
    def parse_object(words, verb):
        try:
            obj = words[1]
            if not verb.transitive:
                raise InvalidUserActionException(f"You can't {verb.name} the {obj}")
        except IndexError:
            if not verb.intransitive:
                raise InvalidUserActionException(f"You need to {verb.name} something") from None
            obj = None
        return obj

    def parse_verb(self, words):
        try:
            verb = self.verbs[words[0]]
        except KeyError:
            raise InvalidUserActionException(f"I don't know how to {words[0]}") from None
        except IndexError:
            raise InvalidUserActionException("Don't give me the silent treatment") from None
        return verb
