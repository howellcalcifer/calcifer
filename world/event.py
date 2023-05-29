from __future__ import annotations

from abc import ABC, abstractmethod

from engine.game import Game
from pattern.observer import Topic, Observer


class Event(ABC):
    @property
    @abstractmethod
    def game(self) -> Game:
        pass


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
