from __future__ import annotations

import dataclasses
from abc import ABC, abstractmethod


@dataclasses.dataclass(frozen=True)
class AttributeChanged:
    subject: Subject
    attribute: str
    value: object


class Observer(ABC):
    """
    The Observer interface declares the update method, used by topics.
    """

    @abstractmethod
    def update(self, event: object) -> None:
        """
        Receive an event from a subject.
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

    def publish(self, event: object) -> None:
        for sub in self._subscribers:
            sub.update(event)


class ObservedAttribute:

    def __get__(self, instance: Subject, _):
        return getattr(instance, self._attr_name)

    def __set__(self, instance: Subject, value):
        setattr(instance, self._attr_name, value)
        instance.publish(AttributeChanged(instance, self._ref_name, value))

    def __set_name__(self, _, name):
        self._attr_name = f'_{name}'
        self._ref_name = name
