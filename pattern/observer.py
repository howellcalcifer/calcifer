from __future__ import annotations

import dataclasses
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar, cast, overload


EventT = TypeVar("EventT")
ValueT = TypeVar("ValueT")


@dataclasses.dataclass(frozen=True)
class AttributeChanged:
    subject: Subject[Any]
    attribute: str
    value: object


class Observer(ABC, Generic[EventT]):
    """
    The Observer interface declares the update method, used by topics.
    """

    @abstractmethod
    def update(self, event: EventT) -> None:
        """
        Receive an event from a subject.
        """
        pass


class Subject(Generic[EventT]):
    """
    The Subject interface declares a set of methods for managing subscribers.
    """

    def __init__(self):
        self._subscribers: list[Observer[EventT]] = []

    def subscribe(self, observer: Observer[EventT]) -> None:
        self._subscribers.append(observer)

    def unsubscribe(self, observer: Observer[EventT]) -> None:
        self._subscribers.remove(observer)

    def publish(self, event: EventT) -> None:
        for sub in self._subscribers:
            sub.update(event)


class ObservedAttribute(Generic[ValueT]):

    def __init__(self) -> None:
        self._attr_name: str
        self._ref_name: str

    @overload
    def __get__(self, instance: None, owner: type[Any]) -> ObservedAttribute[ValueT]: ...

    @overload
    def __get__(self, instance: Subject[AttributeChanged], owner: type[Any]) -> ValueT: ...

    def __get__(self, instance: Subject[AttributeChanged] | None, owner: type[Any]) -> Any:
        if instance is None:
            return self
        return cast(ValueT, getattr(instance, self._attr_name))

    def __set__(self, instance: Subject[AttributeChanged], value: Any) -> None:
        setattr(instance, self._attr_name, value)
        instance.publish(AttributeChanged(instance, self._ref_name, value))

    def __set_name__(self, _, name):
        self._attr_name = f'_{name}'
        self._ref_name = name
