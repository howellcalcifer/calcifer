import abc
import textwrap

from world.character import Character
from world.verb import UserAction, VerbMapping
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

    def await_user_action(self):
        print()
        print("What would you like to do?")
        while True:
            try:
                return self._parser.parse_user_action(input())
            except InvalidUserActionException as e:
                print(e)
                continue

    def set_protagonist(self, protagonist) -> None:
        self._parser.set_protagonist(protagonist)
