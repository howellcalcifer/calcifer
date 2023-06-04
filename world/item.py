from __future__ import annotations

import dataclasses
from typing import Optional

from world.scene import Scene


@dataclasses.dataclass
class Item:
    name: str
    description: Optional[Scene] = None
