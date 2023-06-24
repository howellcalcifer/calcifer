from engine.container_factory import CurrentContainerFactory
from pattern.observer import Subject, ObservedAttribute
from world.character import Character


class Game(Subject):
    protagonist = ObservedAttribute('protagonist')
    running = ObservedAttribute('running')

    def __init__(self):
        super().__init__()
        self.protagonist: Character | None = None
