from __future__ import annotations

from abc import ABC, abstractmethod


class Observer(ABC):
    """
    The Observer interface declares the update method, used by topics.
    """

    @abstractmethod
    def update(self, topic: Subject) -> None:
        """
        Receive update from topic.
        """
        pass


class Subject:
    """
    The Subject interface declares a set of methods for managing subscribers.
    """

    def __init__(self):
        self._subscribers: list[Observer] = []

    def subscribe(self, observer: Observer) -> None:
        self._subscribers.append(observer)

    def unsubscribe(self, observer: Observer) -> None:
        self._subscribers.remove(observer)

    def publish(self) -> None:
        for sub in self._subscribers:
            sub.update(self)
