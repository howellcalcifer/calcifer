from __future__ import annotations

import dataclasses
from typing import Optional

from world.character import Character
from world.item import Item
from world.location import Exit
from world.verb import Verb


@dataclasses.dataclass(frozen=True)
class UserAction:
    verb: Verb
    object: Optional[Item | Character | Exit] = None

    def __hash__(self):
        return hash((self.verb, self.object))


@dataclasses.dataclass
class UnresolvedAction:
    verb: Verb
    object_ref_1: Optional[str] = None
    object_ref_2: Optional[str] = None
