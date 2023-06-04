from __future__ import annotations

import abc
import dataclasses

from pattern.observer import Subject, ObservedAttribute
from world.scene import Scene


class Describable(abc.ABC):
    @property
    @abc.abstractmethod
    def name(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def description(self) -> Scene:
        pass

    @classmethod
    def __subclasshook__(cls, subclass):
        if cls is Describable:
            if any("name" in C.__dict__ for C in subclass.__mro__) and any(
                    "description" in C.__dict__ for C in subclass.__mro__):
                return True
        return NotImplemented


class Character(Subject):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.gesture = None
        self.looking_at = None

    location: Scene = ObservedAttribute('location')
    description: Scene = ObservedAttribute('description')
    looking_at: Describable | None = ObservedAttribute('looking_at')
    gesture: Describable | None = ObservedAttribute('gesture')


@dataclasses.dataclass(frozen=True)
class Gesture:
    name: str
    description: Scene
