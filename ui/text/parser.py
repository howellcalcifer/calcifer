from engine.container_factory import CurrentContainerFactory, CurrentContainerType
from world.character import Character
from world.verb import UserAction, VerbMapping, VerbType


class InvalidUserActionException(Exception):
    pass


class TextParser:
    def __init__(self, verbs: VerbMapping):
        self.verbs = verbs
        self._container_factory = CurrentContainerFactory()

    def parse_user_action(self, text: str) -> UserAction:
        words = text.split()

        try:
            verb = self.verbs[words[0]]
        except KeyError:
            raise InvalidUserActionException(f"I don't know how to {words[0]}") from None
        except IndexError:
            raise InvalidUserActionException("Don't give me the silent treatment") from None

        try:
            obj = self._container_factory.create(CurrentContainerType.VISIBLE)[words[1]]
            if not verb.transitive:
                raise InvalidUserActionException(f"You can't {verb.name} the {obj}")
        except KeyError:
            raise InvalidUserActionException(f"I can't see {words[1]}") from None
        except IndexError:
            if not verb.intransitive:
                raise InvalidUserActionException(f"You need to {verb.name} something") from None
            obj = None
        if verb.type == VerbType.INVENTORY:
            source = self._container_factory.create(verb.source)
            destination = self._container_factory.create(verb.destination)
        else:
            source = None
            destination = None
        return UserAction(verb=verb, object=obj, source=source, destination=destination)

    def set_protagonist(self, protagonist: Character):
        self._container_factory.protagonist = protagonist
