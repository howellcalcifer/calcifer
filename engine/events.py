from __future__ import annotations

import dataclasses

from engine.action import UnresolvedAction, UserAction
from world.character import Character


@dataclasses.dataclass(frozen=True)
class ActionSubmitted:
    action: UnresolvedAction


@dataclasses.dataclass(frozen=True)
class InputRejected:
    error: Exception


@dataclasses.dataclass(frozen=True)
class ActionApplied:
    action: UserAction


@dataclasses.dataclass(frozen=True)
class ActionRejected:
    error: Exception


@dataclasses.dataclass(frozen=True)
class GameStarted:
    protagonist: Character


@dataclasses.dataclass(frozen=True)
class GameStopped:
    pass
