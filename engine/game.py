from engine.action import UserAction
from engine.container_factory import CurrentContainerFactory, CurrentContainerType
from engine.exceptions import InvalidUnresolvedAction
from pattern.observer import Subject, ObservedAttribute
from world.character import Character


class Game(Subject):
    protagonist = ObservedAttribute('protagonist')
    running = ObservedAttribute('running')
    latest_action: UserAction = ObservedAttribute('latest_action')
    latest_rejected_action: InvalidUnresolvedAction = ObservedAttribute('latest_rejected_action')

    def __init__(self):
        super().__init__()
        self.protagonist: Character | None = None
        self._container_factory = CurrentContainerFactory()

    def container(self, typ: CurrentContainerType):
        self._container_factory.protagonist = self.protagonist
        return self._container_factory.create(typ)
