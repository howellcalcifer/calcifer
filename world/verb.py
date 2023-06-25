from __future__ import annotations

import dataclasses
from enum import Enum
from typing import Optional

from engine.container_factory import CurrentContainerType
from world.character import Character
from world.item import Item
from world.location import Exit
from world.scene import Scene


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
    object: Optional[Item | Character | Exit] = None

    def __hash__(self):
        return hash((self.verb, self.object))


