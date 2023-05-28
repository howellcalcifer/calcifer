from __future__ import annotations

import dataclasses
from importlib.resources import files

from world.item import Item
from yaml import load, Loader


@dataclasses.dataclass
class UserVerb:
    name: str


@dataclasses.dataclass
class UserAction:
    verb: UserVerb
    object: Item | None


class UserVerbDictionary(dict[str, UserVerb]):
    @classmethod
    def from_yaml(cls, package: str, resource: str) -> UserVerbDictionary:
        with (files(package) / resource).open('r') as text_io:
            raw_struct = load(text_io, Loader)
        verb_dictionary = UserVerbDictionary()
        try:
            intransitive = raw_struct['intransitive']
            for verb in intransitive:
                verb_dictionary[verb] = UserVerb(verb)
        except KeyError:
            pass
        return verb_dictionary
