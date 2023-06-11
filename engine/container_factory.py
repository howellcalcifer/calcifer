import itertools
from abc import ABC
from enum import Enum
from typing import Optional, Mapping, Iterator

from world.character import Character
from world.item import Item


class CurrentContainerType(Enum):
    PROTAGONIST_ITEMS = 'inventory'
    LOCATION_ITEMS = 'ground'
    LOCATION_CHARACTERS = 'visible_person'
    LOCATION_ALL = 'visible_location'
    ETHER_CHARACTERS = 'ether_person'
    CHARACTER_ITEMS = 'character_inventory'
    ITEM_ITEMS = 'item_inventory'
    VISIBLE = 'visible'


class CurrentContainerFactory(ABC):
    protagonist: Optional[Character]

    def create(self, typ: CurrentContainerType, _: Optional[Item | Mapping] = None) -> Mapping:
        if typ == CurrentContainerType.LOCATION_ITEMS:
            return self.protagonist.location.inventory
        if typ == CurrentContainerType.PROTAGONIST_ITEMS:
            return self.protagonist.inventory
        if typ == CurrentContainerType.VISIBLE:
            subcontainers = [self.protagonist.location.inventory, self.protagonist.inventory]
            return CurrentContainerCombined(subcontainers)


class CurrentContainerCombined(Mapping[str, Item | Character]):

    def __init__(self, subcontainers: list[Mapping]):
        self._subcontainers: list[Mapping[str, Item | Character]] = subcontainers

    def __getitem__(self, key: str) -> Item | Character:
        for container in self._subcontainers:
            try:
                return container[key]
            except KeyError:
                pass
        raise KeyError

    def __len__(self) -> int:
        return sum(len(container) for container in self._subcontainers)

    def __iter__(self) -> Iterator[Item | Character]:
        return itertools.chain(*self._subcontainers)
