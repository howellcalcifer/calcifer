from __future__ import annotations

import dataclasses

from world.scene import Scene


@dataclasses.dataclass
class Item:
    description: Scene