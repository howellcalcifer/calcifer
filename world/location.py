import dataclasses
from typing import Collection

from world.item import Item
from world.scene import Scene


@dataclasses.dataclass
class Location:
    name: str
    items: Collection[Item]
    description_init: dataclasses.InitVar[Scene]

    def __post_init__(self, description_init: Scene):
        self._description = description_init

    @property
    def description(self) -> Scene:
        return Scene(self._description.text)

    @description.setter
    def description(self, scene: Scene):
        self._description = scene
