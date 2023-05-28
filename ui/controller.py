import abc
import textwrap
from typing import Collection

from world.actions import UserAction
from world.scene import Scene
from world.items import Item
from ui.text.parser import TextParser, InvalidUserActionException


class UIController(abc.ABC):
    @abc.abstractmethod
    def show_scene(self, scene: Scene):
        pass

    @abc.abstractmethod
    def await_user_action(self, available_objects=Collection[Item]) -> UserAction:
        pass


class UIControllerCommandLine(UIController):
    def __init__(self, parser: TextParser):
        self.parser = parser

    def show_scene(self, scene: Scene):
        self._output(scene.text)

    def await_user_action(self, available_objects=Collection[Item]):
        print("What would you like to do?")
        while True:
            try:
                return self.parser.parse_user_action(input())
            except InvalidUserActionException:
                print("I don't understand.")
                continue

    @staticmethod
    def _output(string):
        print(textwrap.fill(string, width=76))
