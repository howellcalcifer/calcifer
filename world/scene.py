from __future__ import annotations

import dataclasses
from typing import Collection

from world.items import Item


@dataclasses.dataclass
class Scene:
    text: str
    items: Collection[Item]
