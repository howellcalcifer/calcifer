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

        if not verb.intransitive:
            try:
                return UserAction(verb=verb, object=self.visible_entities[words[1]])
            except KeyError:
                raise InvalidUserActionException(f"I can't see {words[1]}") from None
            except IndexError:
                raise InvalidUserActionException(f"You need to {verb.name} something") from None
        return UserAction(verb=verb)
