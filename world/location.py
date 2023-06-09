from __future__ import annotations
import dataclasses

from world.item import Inventory
from world.scene import Scene


class Direction(str):
    pass


@dataclasses.dataclass
class Exit:
    direction: Direction
    leads_to: Location


@dataclasses.dataclass
class Location:
    name: str
    inventory: Inventory
    description_init: dataclasses.InitVar[Scene]
    exits: dict[Direction, Exit] = dataclasses.field(default_factory=dict)

    def __post_init__(self, description_init: Scene):
        self._description = description_init

    @property
    def description(self) -> Scene:
        item_text = ",".join(f"{self._item_article(i > 0, item)} {item}" for i, item in enumerate(self.inventory))
        return Scene(f"{self._description.text}\n{item_text} is here." if item_text else self._description.text)

    @staticmethod
    def _item_article(capitalise: bool, _):
        return 'a' if capitalise else 'A'

    @description.setter
    def description(self, scene: Scene):
        self._description = scene

    def __hash__(self):
        return hash(self.name)
