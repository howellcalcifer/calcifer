from __future__ import annotations

import dataclasses
from abc import ABC

from world.scene import Scene


@dataclasses.dataclass
class Item(ABC):
    name: str
    description: Scene
