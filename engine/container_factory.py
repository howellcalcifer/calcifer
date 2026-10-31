from enum import Enum
from collections.abc import Iterator, Mapping

from world.character import Character
from world.item import Item
from world.location import Exit


class CurrentContainerType(Enum):
    PROTAGONIST_ITEMS = 'inventory'
    LOCATION_ITEMS = 'ground'
    LOCATION_CHARACTERS = 'visible_person'
    LOCATION_EXITS = 'exits'
    CHARACTER_ITEMS = 'character_inventory'
    ITEM_ITEMS = 'item_inventory'
    VISIBLE = 'visible'


class CurrentContainerFactory:
    protagonist: Character | None

    def create(self, typ: CurrentContainerType) -> Mapping[str, Item | Character | Exit]:
        protagonist = self.protagonist
        if protagonist is None:
            raise RuntimeError("The game has no protagonist")
        if typ == CurrentContainerType.LOCATION_ITEMS:
            return protagonist.location.inventory
        if typ == CurrentContainerType.PROTAGONIST_ITEMS:
            return protagonist.inventory
        if typ == CurrentContainerType.LOCATION_EXITS:
            return protagonist.location.exits
        if typ == CurrentContainerType.VISIBLE:
            subcontainers: list[Mapping[str, Item | Character | Exit]] = [
                protagonist.location.inventory,
                protagonist.inventory,
                protagonist.location.exits,
            ]
            return CurrentContainerCombined(subcontainers)
        raise ValueError(f"Unsupported container type: {typ}")


class CurrentContainerCombined(Mapping[str, Item | Character | Exit]):

    def __init__(self, subcontainers: list[Mapping[str, Item | Character | Exit]]):
        self._subcontainers = subcontainers

    def __getitem__(self, key: str) -> Item | Character | Exit:
        for container in self._subcontainers:
            try:
                return container[key]
            except KeyError:
                pass
        raise KeyError

    def __len__(self) -> int:
        return sum(len(container) for container in self._subcontainers)

    def __iter__(self) -> Iterator[str]:
        for container in self._subcontainers:
            yield from container
