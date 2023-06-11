from __future__ import annotations

import dataclasses
from enum import Enum
from importlib.resources import files
from typing import Optional

from yaml import load, Loader

from engine.container_factory import CurrentContainerType
from world.character import Character
from world.item import Item, Inventory
from world.scene import Scene


class CoreVerbs(Enum):
    LOOK = "look"
    QUIT = "quit"


class VerbType(Enum):
    LOOK = "look"
    GESTURE = "gesture"
    POSTURE = "posture"
    MAGIC = "magic"
    INVENTORY = "inventory"
    MOVE = "move"
    QUIT = "quit"


@dataclasses.dataclass(frozen=True)
class Verb:
    name: str
    type: VerbType
    description: Optional[Scene]
    transitive: Optional[bool]
    intransitive: Optional[bool]

    def __hash__(self):
        return hash(self.name)

    @classmethod
    def create(cls, name: str, type: VerbType, *args, **kwargs) -> Verb:
        match type:
            case VerbType.INVENTORY:
                return InventoryVerb(name, type, *args, **kwargs)
            case _:
                return cls(name, type, *args, **kwargs)


@dataclasses.dataclass(frozen=True)
class InventoryVerb(Verb):
    source: CurrentContainerType
    destination: CurrentContainerType


@dataclasses.dataclass(frozen=True)
class UserAction:
    verb: Verb
    object: Optional[Item | Character] = None
    source: Optional[Inventory] = None
    destination: Optional[Inventory] = None

    def __hash__(self):
        return hash((self.verb, self.object))


class VerbMapping(dict[str, Verb]):
    @classmethod
    def from_yaml(cls, package: str, resource: str) -> VerbMapping:
        with (files(package) / resource).open('r') as text_io:
            raw_struct = load(text_io, Loader)
        verb_dictionary = VerbMapping()

        for verb, properties in raw_struct.items():
            verb_args = (verb, VerbType(properties["type"]),
                         Scene(properties["description"] if "description" in properties else None),
                         properties[
                             "transitive"] if "transitive" in properties else None,
                         properties[
                             "intransitive"] if "intransitive" in properties else None)
            for prop in ["source", "destination"]:
                try:
                    verb_args = verb_args + (CurrentContainerType(properties[prop]),)
                except KeyError:
                    pass

            verb_dictionary[verb] = Verb.create(*verb_args)

        return verb_dictionary
