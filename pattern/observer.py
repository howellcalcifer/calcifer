from __future__ import annotations

from abc import ABC, abstractmethod


class Observer(ABC):
    """
    The Observer interface declares the update method, used by topics.
    """

    @abstractmethod
    def update(self, topic: Topic) -> None:
        """
        Receive update from topic.
        """
        pass


class Topic(ABC):
    """
    The Topic interface declares a set of methods for managing subscribers.
    """

    @abstractmethod
    def subscribe(self, observer: Observer) -> None:
        """
        Attach an observer to the topic.
        """
        pass

    @abstractmethod
    def unsubscribe(self, observer: Observer) -> None:
        """
        Detach an observer from the topic.
        """
        pass

    @abstractmethod
    def publish(self) -> None:
        """
        Notify all observers about an event.
        """
        pass
