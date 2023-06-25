from __future__ import annotations

import dataclasses


@dataclasses.dataclass(frozen=True)
class Scene:
    text: str
