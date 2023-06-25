import abc
import textwrap

from engine.container_factory import CurrentContainerType
from engine.game import Game
from pattern.observer import Subject, ObservedAttribute
from ui.text.parser import TextParser, InvalidUserActionException
from world.mappings import VerbMapping
from world.scene import Scene
from world.verb import UserAction, VerbType


class OutputController(abc.ABC):
    @abc.abstractmethod
    def show_scene(self, scene: Scene):
        pass


class InputController(Subject, abc.ABC):

    @property
    @abc.abstractmethod
    def action(self) -> UserAction:
        pass

    @abc.abstractmethod
    def await_user_action(self) -> UserAction:
        pass

    @abc.abstractmethod
    def start(self) -> None:
        pass


class OutputException(Exception):
    pass


class OutputControllerCommandLine(OutputController):
    def show_scene(self, scene: Scene):
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
        self._action = None

    action = ObservedAttribute('action')

    def await_user_action(self):
        while True:
            try:
                parsed = self._parser.parse_user_action(input())
            except InvalidUserActionException as e:
                print(e)
                continue

            if parsed.object_ref_1 is None:
                if parsed.verb.type != VerbType.LOOK:
                    self.action = UserAction(verb=parsed.verb)
                else:
                    self.action = UserAction(verb=parsed.verb, object=self._game.protagonist.location)
                return

            visible_objects = self._game.container(CurrentContainerType.VISIBLE)
            try:
                obj = visible_objects[parsed.object_ref_1]
            except KeyError:
                print(f"You can't see any {parsed.object_ref_1}")
                continue
            if parsed.verb.type == VerbType.INVENTORY:
                source = self._game.container(parsed.verb.source)
                destination = self._game.container(parsed.verb.destination)
                try:
                    if obj.name not in source or obj.name in destination:
                        print(f"You can't {parsed.verb.name} that.")
                        continue
                except AttributeError:
                    print(f"You can't {parsed.verb.name} that.")
                    continue
            if parsed.verb.type == VerbType.MOVE:
                try:
                    if obj.direction not in self._game.container(CurrentContainerType.LOCATION_EXITS):
                        print(f"You can't go {obj.direction}")
                        continue
                except AttributeError:
                    print("You can't go there.")
                    continue
            self.action = UserAction(verb=parsed.verb, object=obj)
            return

    def start(self):
        while self._game.running:
            self.await_user_action()
