import dataclasses

from world.item import Inventory
from world.scene import Scene


@dataclasses.dataclass
class Location:
    name: str
    inventory: Inventory
    description_init: dataclasses.InitVar[Scene]

    def __post_init__(self, description_init: Scene):
        self._description = description_init

    @property
    def description(self) -> Scene:
        item_text = ",".join(f"{self._item_article(i > 0, item)} {item}" for i, item in enumerate(self.inventory))
        return Scene(f"{self._description.text}\n\n{item_text} is here." if item_text else self._description.text)

    @staticmethod
    def _item_article(capitalise: bool, _):
        return 'a' if capitalise else 'A'

    @description.setter
    def description(self, scene: Scene):
        self._description = scene

    def __hash__(self):
        return hash(self.name)


