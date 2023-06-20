from engine.container_factory import CurrentContainerFactory
from pattern.observer import Subject, ObservedAttribute
from ui.controllers import InputController
from world.character import Character, Gesture
from world.scene import Scene
from world.verb import VerbType


class Game(Subject):
    failure_status: str = ObservedAttribute('failure_status')

    def __init__(self, input: InputController):
        super().__init__()
        self._input = input
        self._protagonist: Character | None = None
        self._current_containers = CurrentContainerFactory()

    def start(self):
        self.protagonist.looking_at = self.protagonist
        while True:
            action = self._input.await_user_action()
            match action.verb.type:
                case VerbType.LOOK:
                    self.protagonist.looking_at = self.protagonist.location
                case VerbType.GESTURE:
                    self.protagonist.gesture = Gesture(name=action.verb.name,
                                                    description=action.verb.description
                                                    if action.verb.description else Scene(f"You {action.verb.name}"))
                case VerbType.QUIT:
                    print("Goodbye for now.")
                    break
                case VerbType.INVENTORY:
                    source = self._current_containers.create(action.verb.source)
                    destination = self._current_containers.create(action.verb.destination)
                    source.remove(action.object)
                    destination.add(action.object)
                case _:
                    self.failure_status = "I don't understand what you mean."

    @property
    def protagonist(self):
        return self._protagonist

    @protagonist.setter
    def protagonist(self, protagonist: Character):
        self._protagonist = protagonist
        self._input.set_protagonist(protagonist)
        self._current_containers.protagonist = protagonist



