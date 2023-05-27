from __future__ import annotations

import dataclasses
from typing import Collection


@dataclasses.dataclass
class Scene:
    text: str
    visible_objects: Collection[SceneObject]


@dataclasses.dataclass
class SceneObject:
    description: Scene
