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

    @property
    def description(self) -> Scene:
        return Scene(f"The way {self.direction} leads to {self.leads_to.name}.")


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
