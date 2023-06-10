from __future__ import annotations

import abc
import dataclasses

from pattern.observer import Subject, ObservedAttribute
from world.scene import Scene


class Describable(abc.ABC):

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """ the name of the entity"""

    @property
    @abc.abstractmethod
    def description(self) -> Scene:
        """ the scene describing the entity"""

    @classmethod
    def __subclasshook__(cls, subclass):
        if cls is Describable:
            return cls._has_attribute(subclass, "name") and cls._has_attribute(subclass, "description")
        return NotImplemented

    @staticmethod
    def _has_attribute(subclass, attr_name) -> bool:
        return any(
            (attr_name in (dict([(f.name, f) for f in dataclasses.fields(C)])) | C.__dict__) if dataclasses.is_dataclass(C)
            else attr_name in C.__dict__
            for C in subclass.__mro__)


class Character(Subject):
    def __init__(self, name):
        super().__init__()
        self._name = name
        self.gesture = None
        self.looking_at = None

    location: Scene = ObservedAttribute('location')
    description: Scene = ObservedAttribute('description')
    looking_at: Describable | None = ObservedAttribute('looking_at')
    gesture: Describable | None = ObservedAttribute('gesture')

    @property
    def name(self):
        return self._name


@dataclasses.dataclass(frozen=True)
class Gesture:
    name: str
    description: Scene
