import dataclasses
from typing import Optional

from world.verb import Verb
from world.mappings import VerbMapping


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

    def parse_user_action(self, text: str) -> ParsedResult:
        words = text.split()
        verb = self.parse_verb(words)
        obj = self.parse_object(words, verb)
        return ParsedResult(verb=verb, object_ref_1=obj)

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
