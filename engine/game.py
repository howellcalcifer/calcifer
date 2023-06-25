from engine.container_factory import CurrentContainerFactory, CurrentContainerType
from pattern.observer import Subject, ObservedAttribute
from world.character import Character
from world.verb import UserAction


class Game(Subject):
    protagonist = ObservedAttribute('protagonist')
    running = ObservedAttribute('running')
    latest_action: UserAction = ObservedAttribute('latest_action')

    def __init__(self):
        super().__init__()
        self.protagonist: Character | None = None
        self._container_factory = CurrentContainerFactory()

    def container(self, typ: CurrentContainerType):
        self._container_factory.protagonist = self.protagonist
        return self._container_factory.create(typ)
