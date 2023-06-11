from __future__ import annotations

import dataclasses
from importlib.resources import files
from typing import Optional, Iterator, MutableMapping, Dict

from yaml import load, Loader

from pattern.observer import Subject
from world.scene import Scene


@dataclasses.dataclass
class Item:
    name: str
    description: Optional[Scene] = None
    display_name: Optional[str] = None

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.display_name if self.display_name else self.name


class ItemMapping(dict[str, Item]):
    @classmethod
    def from_yaml(cls, package: str, resource: str) -> ItemMapping:
        with (files(package) / resource).open('r') as text_io:
            raw_struct = load(text_io, Loader)
        item_mapping = ItemMapping()
        for name, properties in raw_struct.items():
            args = (name,)
            kwargs = {}
            for prop in ['description', 'display_name']:
                try:
                    kwargs[prop] = properties[prop]
                except KeyError:
                    pass
            item_mapping[name] = Item(*args, **kwargs)
        return item_mapping


class Inventory(MutableMapping[str, Item], Subject):

    def __init__(self):
        super().__init__()
        self._items: Dict[str, Item] = dict()
        self.item_incoming: Optional[Item] = None
        self.item_outgoing: Optional[Item] = None

    def __len__(self) -> int:
        return self._items.__len__()

    def __iter__(self) -> Iterator[str]:
        return self._items.__iter__()

    def __contains__(self, __x: str) -> bool:
        return self._items.__contains__(__x)

    def __getitem__(self, __x: str):
        return self._items.__getitem__(__x)

    def __delitem__(self, key: str) -> None:
        self.item_outgoing = self._items[key]
        self.publish()
        print(f"Removing item {key}")
        del self._items[key]
        self.item_outgoing = None

    def __setitem__(self, key: str, item: Item) -> None:
        self.item_incoming = item
        self.publish()
        print(f"Adding item {key}")
        self._items[key] = item
        self.item_incoming = None

    def add(self, item: Item) -> None:
        self.__setitem__(item.name, item)

    def remove(self, item: Item) -> None:
        self.__delitem__(item.name)
