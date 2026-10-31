import abc
import textwrap

from engine.action import UnresolvedAction
from engine.events import ActionSubmitted, InputEvent, InputRejected
from engine.game import Game
from pattern.observer import Subject
from ui.text.parser import TextParser, InvalidUserActionException
from world.mappings import VerbMapping
from world.scene import Scene


class OutputController(abc.ABC):
    @abc.abstractmethod
    def show_scene(self, scene: Scene | None) -> None:
        pass


class InputController(Subject[InputEvent], abc.ABC):

    @abc.abstractmethod
    def await_user_action(self) -> UnresolvedAction:
        pass

    @abc.abstractmethod
    def start(self) -> None:
        pass


class OutputException(Exception):
    pass


class OutputControllerCommandLine(OutputController):
    def show_scene(self, scene: Scene | None) -> None:
        if scene is None:
            raise OutputException("Trying to show a non-existent scene")
        if scene.text is None:
            raise OutputException("Trying to show a scene without any text")
        self._output(scene.text)

    @staticmethod
    def _output(string):
        lines = ["\n".join(textwrap.wrap(line, 76)) for line in string.strip().split("\n")]
        print("\n".join(lines))


class InputControllerCommandLine(InputController):

    def __init__(self, verbs: VerbMapping, game: Game):
        super().__init__()
        self._parser = TextParser(verbs)
        self._game = game

    def await_user_action(self):
        while True:
            try:
                action = self._parser.parse_user_action(input())
            except InvalidUserActionException as e:
                self.publish(InputRejected(e))
                continue
            self.publish(ActionSubmitted(action))
            return action

    def start(self):
        while self._game.running:
            self.await_user_action()
