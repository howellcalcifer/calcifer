import dataclasses

from ui.scene import SceneObject


@dataclasses.dataclass
class UserVerb:
    name: str


@dataclasses.dataclass
class UserAction:
    verb: UserVerb
    object: SceneObject | None
