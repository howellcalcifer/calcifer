import abc
import textwrap

from engine.container_factory import CurrentContainerFactory, CurrentContainerType
from world.character import Character
from world.verb import UserAction, VerbType
from world.mappings import VerbMapping
from world.scene import Scene
from ui.text.parser import TextParser, InvalidUserActionException


class OutputController(abc.ABC):
    @abc.abstractmethod
    def show_scene(self, scene: Scene):
        pass


class InputController(abc.ABC):
    @abc.abstractmethod
    def await_user_action(self) -> UserAction:
        pass

    @abc.abstractmethod
    def set_protagonist(self, protagonist: Character) -> None:
        pass


class OutputControllerCommandLine(OutputController):
    def show_scene(self, scene: Scene):
        self._output(scene.text)

    @staticmethod
    def _output(string):
        lines = ["\n".join(textwrap.wrap(line, 76)) for line in string.strip().split("\n")]
        print("\n".join(lines))


class InputControllerCommandLine(InputController):

    def __init__(self, verbs: VerbMapping):
        self._parser = TextParser(verbs)
        self._container_factory = CurrentContainerFactory()

    def await_user_action(self):
        print()
        print("What would you like to do?")
        while True:
            try:
                parsed = self._parser.parse_user_action(input())
            except InvalidUserActionException as e:
                print(e)
                continue

            if parsed.object_ref_1 is None:
                return UserAction(verb=parsed.verb)

            visible_objects = self._container_factory.create(CurrentContainerType.VISIBLE)
            try:
                obj = visible_objects[parsed.object_ref_1]
            except KeyError:
                print(f"You can't see any {parsed.object_ref_1}")
                continue
            if parsed.verb.type == VerbType.INVENTORY:
                source = self._container_factory.create(parsed.verb.source)
                destination = self._container_factory.create(parsed.verb.destination)
                if obj.name not in source or obj.name in destination:
                    print(f"You can't {parsed.verb.name} the {obj}")
                    continue
            return UserAction(verb=parsed.verb, object=obj)

    def set_protagonist(self, protagonist) -> None:
        self._container_factory.protagonist = protagonist
