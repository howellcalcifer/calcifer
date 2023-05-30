from __future__ import annotations

import dataclasses
from enum import Enum
from importlib.resources import files

from yaml import load, Loader

from world.item import Item


class CoreVerbs(Enum):
    LOOK = "look"
    QUIT = "quit"


@dataclasses.dataclass(frozen=True)
class UserVerb:
    name: str


@dataclasses.dataclass(frozen=True)
class UserAction:
    verb: UserVerb
    object: Item | None


class UserVerbDict(dict[str, UserVerb]):
    @classmethod
    def from_yaml(cls, package: str, resource: str) -> UserVerbDict:
        with (files(package) / resource).open('r') as text_io:
            raw_struct = load(text_io, Loader)
        verb_dictionary = UserVerbDict()

        intransitive = raw_struct['intransitive']

        for verb in intransitive:
            verb_dictionary[verb] = UserVerb(verb)
        return verb_dictionary


