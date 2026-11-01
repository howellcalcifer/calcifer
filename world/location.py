from __future__ import annotations
import dataclasses
from enum import StrEnum

from world.item import Inventory
from world.scene import Scene


class Direction(StrEnum):
    shortcut: str

    def __new__(cls, value: str, shortcut: str = ""):
        direction = str.__new__(cls, value)
        direction._value_ = value
        direction.shortcut = shortcut
        return direction

    NORTH = ("north", "n")
    SOUTH = ("south", "s")
    EAST = ("east", "e")
    WEST = ("west", "w")
    NORTHWEST = ("northwest", "nw")
    NORTHEAST = ("northeast", "ne")
    SOUTHWEST = ("southwest", "sw")
    SOUTHEAST = ("southeast", "se")

    @classmethod
    def from_shortcut(cls, shortcut: str) -> Direction | None:
        return next((direction for direction in cls if direction.shortcut == shortcut), None)

    @classmethod
    def from_name(cls, name: str) -> Direction | None:
        return next((direction for direction in cls if direction.value == name), None)


@dataclasses.dataclass
class Exit:
    direction: Direction
    leads_to: Location

    def __post_init__(self) -> None:
        self.direction = Direction(self.direction)

    @property
    def description(self) -> Scene:
        return Scene(f"The way {self.direction.value} leads to {self.leads_to.name}.")


@dataclasses.dataclass
class Location:
    name: str
    inventory: Inventory
    description_init: dataclasses.InitVar[Scene]
    exits: dict[str, Exit] = dataclasses.field(default_factory=dict)

    def __post_init__(self, description_init: Scene) -> None:
        self._description = description_init

    def _get_description(self) -> Scene:
        item_text = ",".join(f"{self._item_article(i > 0, item)} {item}" for i, item in enumerate(self.inventory))
        description = self._description.text
        if item_text:
            description += f"\n{item_text} is here."
        if self.exits:
            description += f"\nExits: {', '.join(sorted(self.exits))}"
        return Scene(description)

    def _set_description(self, scene: Scene) -> None:
        self._description = scene

    description = property(_get_description, _set_description)

    @staticmethod
    def _item_article(capitalise: bool, _):
        return 'a' if capitalise else 'A'

    def __hash__(self):
        return hash(self.name)
