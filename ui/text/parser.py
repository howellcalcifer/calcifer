from engine.container_factory import CurrentContainerFactory, CurrentContainerType
from world.character import Character
from world.verb import UserAction, VerbMapping, VerbType


class InvalidUserActionException(Exception):
    pass


class TextParser:
    def __init__(self, verbs: VerbMapping):
        self.verbs = verbs
        # TODO: move this up to controller, with all its logic
        self._container_factory = CurrentContainerFactory()

    def parse_user_action(self, text: str) -> UserAction:
        words = text.split()
        verb = self.parse_verb(words)
        obj = self.parse_object(words, verb)
        destination, source = self.parse_inventory_move(verb, obj)
        return UserAction(verb=verb, object=obj, source=source, destination=destination)

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

    def parse_object(self, words, verb):
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
        return obj

    def parse_verb(self, words):
        try:
            verb = self.verbs[words[0]]
        except KeyError:
            raise InvalidUserActionException(f"I don't know how to {words[0]}") from None
        except IndexError:
            raise InvalidUserActionException("Don't give me the silent treatment") from None
        return verb

    # TODO: move this up to controller
    def set_protagonist(self, protagonist: Character):

        self._container_factory.protagonist = protagonist
