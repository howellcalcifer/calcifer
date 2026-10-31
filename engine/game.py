from engine.container_factory import CurrentContainerFactory, CurrentContainerType
from engine.events import GameStarted, GameStopped
from pattern.observer import Subject
from world.character import Character


class Game(Subject):
    def __init__(self):
        super().__init__()
        self.protagonist: Character | None = None
        self.running = False
        self._container_factory = CurrentContainerFactory()

    def start(self, protagonist: Character) -> None:
        self.protagonist = protagonist
        self.running = True
        self.publish(GameStarted(protagonist))

    def stop(self) -> None:
        self.running = False
        self.publish(GameStopped())

    def container(self, typ: CurrentContainerType):
        self._container_factory.protagonist = self.protagonist
        return self._container_factory.create(typ)
