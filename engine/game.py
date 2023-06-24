from engine.container_factory import CurrentContainerFactory
from pattern.observer import ObservedAttribute
from world.character import Character


class Game:
    failure_status: str = ObservedAttribute('failure_status')

    def __init__(self):
        super().__init__()
        self._protagonist: Character | None = None
        self._current_containers = CurrentContainerFactory()
        self.running = True

    @property
    def protagonist(self):
        return self._protagonist

    @protagonist.setter
    def protagonist(self, protagonist: Character):
        self._protagonist = protagonist
        self._current_containers.protagonist = protagonist

