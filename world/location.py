import dataclasses
from typing import Collection

from world.item import Item
from world.scene import Scene


@dataclasses.dataclass
class Location:
    name: str
    description: Scene
    items: Collection[Item]
