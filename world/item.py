from __future__ import annotations

import dataclasses
from typing import Optional, Collection, Iterator, Set

from pattern.observer import Subject
from world.scene import Scene


@dataclasses.dataclass
class Item:
    name: str
    description: Optional[Scene] = None

    def __hash__(self):
        return hash(self.name)


class Inventory(Collection[Item], Subject):

    def __init__(self):
        super().__init__()
        self._items: Set[Item] = set()
        self.item_incoming: Optional[Item] = None
        self.item_outgoing: Optional[Item] = None

    def __len__(self) -> int:
        return self._items.__len__()

    def __iter__(self) -> Iterator[Item]:
        return self._items.__iter__()

    def __contains__(self, __x: object) -> bool:
        return self._items.__contains__(__x)

    def add(self, item: Item):
        self.item_incoming = item
        self.publish()
        self._items.add(item)
        self.item_incoming = None

    def remove(self, item: Item):
        self.item_outgoing = item
        self.publish()
        self._items.remove(item)
        self.item_outgoing = None
