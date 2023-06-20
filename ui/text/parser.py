import dataclasses
from typing import Optional

from world.verb import VerbMapping, Verb


class InvalidUserActionException(Exception):
    pass


@dataclasses.dataclass
class ParsedResult:
    verb: Verb
    object_ref_1: Optional[str] = None
    object_ref_2: Optional[str] = None


class TextParser:
    def __init__(self, verbs: VerbMapping):
        self.verbs = verbs
        # TODO: move this up to controller, with all its logic

    def parse_user_action(self, text: str) -> ParsedResult:
        words = text.split()
        verb = self.parse_verb(words)
        obj = self.parse_object(words, verb)
        return ParsedResult(verb=verb, object_ref_1=obj)

    """
    def parse_inventory_move(self, verb, obj):
        if verb.type == VerbType.INVENTORY:
            source = self._container_factory.create(verb.source)
            destination = self._container_factory.create(verb.destination)
            if obj.name not in source or obj.name in destination:
                raise InvalidUserActionException(f"You can't {verb.name} the {obj}")
        else:
            source = None
            destination = None
        return destination, source
    """

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

