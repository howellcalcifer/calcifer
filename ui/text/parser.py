from world.character import Character
from world.item import Item
from world.verb import UserAction, UserVerbDict


class InvalidUserActionException(Exception):
    pass


class TextParser:
    def __init__(self, verbs: UserVerbDict):
        self.verbs = verbs
        self.visible_entities: dict[str, Item | Character] = {}

    def parse_user_action(self, text: str) -> UserAction:
        words = text.split()

        try:
            verb = self.verbs[words[0]]
        except KeyError:
            raise InvalidUserActionException(f"I don't know how to {words[0]}") from None
        except IndexError:
            raise InvalidUserActionException("Don't give me the silent treatment") from None

        try:
            obj = self.visible_entities[words[1]]
            if not verb.transitive:
                raise InvalidUserActionException(f"You can't {verb.name} the {obj}")
        except KeyError:
            raise InvalidUserActionException(f"I can't see {words[1]}") from None
        except IndexError:
            if not verb.intransitive:
                raise InvalidUserActionException(f"You need to {verb.name} something") from None
            obj = None
        return UserAction(verb=verb, object=obj)
