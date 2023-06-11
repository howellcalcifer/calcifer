from __future__ import annotations

import abc
import dataclasses
from importlib.resources import files
from typing import Optional

from yaml import load, Loader

from pattern.observer import Subject, ObservedAttribute
from world.item import Inventory, ItemMapping
from world.location import Location
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
            (attr_name in (
                dict([(f.name, f) for f in dataclasses.fields(C)])) | C.__dict__) if dataclasses.is_dataclass(C)
            else attr_name in C.__dict__
            for C in subclass.__mro__)


class Character(Subject):
    def __init__(self, name: str, inventory: Inventory, display_name: str | None = None,
                 description: Scene | None = None):
        super().__init__()
        self._name: str = name
        self.gesture: Optional[Gesture] = None
        self.looking_at: Optional[Describable] = None
        self.inventory: Inventory = inventory
        self._display_name = display_name
        self._description = description

    location: Location = ObservedAttribute('location')
    looking_at: Optional[Describable] = ObservedAttribute('looking_at')
    gesture: Optional[Describable] = ObservedAttribute('gesture')

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    def __hash__(self):
        return hash(self.name)


class CharacterMapping(dict[str, Character]):

    @classmethod
    def from_yaml(cls, package: str, resource: str, items: ItemMapping) -> CharacterMapping:
        with (files(package) / resource).open('r') as text_io:
            raw_struct = load(text_io, Loader)
        mapping = cls()
        for name, properties in raw_struct.items():
            inventory = cls.load_inventory(properties, items)
            args = (name, inventory)
            kwargs = {}
            for prop in ['description', 'display_name']:
                try:
                    kwargs[prop] = properties[prop]
                except KeyError:
                    pass
            mapping[name] = Character(*args, **kwargs)
        return mapping

    @staticmethod
    def load_inventory(yaml_character, items):
        inventory = Inventory()
        if 'inventory' in yaml_character:
            for item_name in yaml_character['inventory']:
                inventory.add(items[item_name])
        return inventory


@dataclasses.dataclass(frozen=True)
class Gesture:
    name: str
    description: Scene
