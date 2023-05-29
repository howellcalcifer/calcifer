from __future__ import annotations

import dataclasses

from engine.game import Game
from pattern.observer import Topic, Observer
from world.action import UserAction


@dataclasses.dataclass
class Event:
    game: Game
    action: UserAction


class EventTopic(Topic):
    _subscribers: list[Observer] = []
    event: Event

    def subscribe(self, observer: Observer) -> None:
        self._subscribers.append(observer)

    def unsubscribe(self, observer: Observer) -> None:
        self._subscribers.remove(observer)

    def publish(self) -> None:
        for sub in self._subscribers:
            sub.update(self)
