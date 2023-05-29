import dataclasses
from abc import ABC, abstractmethod

from world.location import Location
from world.scene import Scene


class Character(ABC):

    @property
    @abstractmethod
    def location(self) -> Location:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass


class Calcifer(Character):
    _location: Location

    def __init__(self, location: Location):
        self._location = location

    @property
    def location(self):
        return self._location

    @property
    def description(self) -> Scene:
        return Scene("You are Calcifer. You have a thin blue face, a thin blue nose, curly green flames for hair"
                     "and eyebrows, a purple flaming mouth, and savage teeth. Your eyes are orange flames with"
                     "purple pupils. You do not have any evident lower body.")
