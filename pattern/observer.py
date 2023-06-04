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
        self.changed_observed_attribute = None

    def subscribe(self, observer: Observer) -> None:
        self._subscribers.append(observer)

    def unsubscribe(self, observer: Observer) -> None:
        self._subscribers.remove(observer)

    def publish(self, channel=None) -> None:
        for sub in self._subscribers:
            sub.update(self)
        self.changed_observed_attribute = None


class ObservedAttribute:

    def __init__(self, channel):
        self._channel = channel

    def __get__(self, instance: Subject, _):
        return getattr(instance, self._attr_name)

    def __set__(self, instance: Subject, value):
        instance.changed_observed_attribute = self._ref_name
        setattr(instance, self._attr_name, value)
        instance.publish(self._channel)

    def __set_name__(self, _, name):
        self._attr_name = f'_{name}'
        self._ref_name = name
