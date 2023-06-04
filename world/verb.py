from __future__ import annotations

import dataclasses
from enum import Enum
from importlib.resources import files
from typing import Optional

from yaml import load, Loader

from world.character import Character
from world.item import Item
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
class UserVerb:
    name: str
    type: VerbType
    description: Optional[Scene] = None
    transitive: Optional[bool] = None
    intransitive: Optional[bool] = None


@dataclasses.dataclass(frozen=True)
class UserAction:
    verb: UserVerb
    object: Optional[Item | Character] = None


class UserVerbDict(dict[str, UserVerb]):
    @classmethod
    def from_yaml(cls, package: str, resource: str) -> UserVerbDict:
        with (files(package) / resource).open('r') as text_io:
            raw_struct = load(text_io, Loader)
        verb_dictionary = UserVerbDict()

        for verb, properties in raw_struct.items():
            verb_dictionary[verb] = UserVerb(verb, VerbType(properties["type"]),
                                             Scene(properties["description"]) if "description" in properties else None,
                                             transitive=properties[
                                                 "transitive"] if "transitive" in properties else None,
                                             intransitive=properties[
                                                 "intransitive"] if "intransitive" in properties else None
                                             )
        return verb_dictionary
