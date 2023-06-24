from __future__ import annotations

from importlib.resources import files

from yaml import load, Loader

from engine.container_factory import CurrentContainerType
from world.character import Character
from world.item import Inventory, Item
from world.location import Location
from world.scene import Scene
from world.verb import Verb, VerbType


class LocationMapping(dict[str, Location]):

    @classmethod
    def from_yaml(cls, package: str, resource: str, items: ItemMapping, _: CharacterMapping) -> LocationMapping:
        with (files(package) / resource).open('r') as text_io:
            raw_struct = load(text_io, Loader)
        mapping = cls()
        for name, properties in raw_struct.items():
            inventory = cls.load_inventory(properties, items)
            args = (name, inventory)
            kwargs = {}
            try:
                kwargs['description_init'] = Scene(properties['description'])
            except KeyError:
                pass
            mapping[name] = Location(*args, **kwargs)
        return mapping

    @staticmethod
    def load_inventory(yaml_character, items):
        inventory = Inventory()
        if 'inventory' in yaml_character:
            for item_name in yaml_character['inventory']:
                inventory.add(items[item_name])
        return inventory


class CharacterMapping(dict[str, Character]):

    @classmethod
    def from_yaml(cls, package: str, resource: str, items: ItemMapping) -> CharacterMapping:
        with (files(package) / resource).open('r') as text_io:
            raw_struct = load(text_io, Loader)
        mapping = cls()
        for name, properties in raw_struct.items():
            inventory = cls.load_inventory(properties, items)
            args = (name, inventory)
            kwargs = {}
            try:
                kwargs['description'] = Scene(properties['description'])
            except KeyError:
                pass
            try:
                kwargs['display_name'] = properties['display_name']
            except KeyError:
                pass
            mapping[name] = Character(*args, **kwargs)
        return mapping

    @staticmethod
    def load_inventory(yaml_character, items):
        inventory = Inventory()
        if 'inventory' in yaml_character:
            for item_name in yaml_character['inventory']:
                inventory.add(items[item_name])
        return inventory


class ItemMapping(dict[str, Item]):
    @classmethod
    def from_yaml(cls, package: str, resource: str) -> ItemMapping:
        with (files(package) / resource).open('r') as text_io:
            raw_struct = load(text_io, Loader)
        item_mapping = ItemMapping()
        for name, properties in raw_struct.items():
            args = (name,)
            kwargs = {}
            try:
                kwargs['description'] = Scene(properties['description'])
            except KeyError:
                pass
            try:
                kwargs['display_name'] = properties['display_name']
            except KeyError:
                pass
            item_mapping[name] = Item(*args, **kwargs)
        return item_mapping


class VerbMapping(dict[str, Verb]):
    @classmethod
    def from_yaml(cls, package: str, resource: str) -> VerbMapping:
        with (files(package) / resource).open('r') as text_io:
            raw_struct = load(text_io, Loader)
        verb_dictionary = VerbMapping()

        for verb, properties in raw_struct.items():
            verb_args = (verb, VerbType(properties["type"]),
                         Scene(properties["description"]) if "description" in properties else None,
                         properties[
                             "transitive"] if "transitive" in properties else None,
                         properties[
                             "intransitive"] if "intransitive" in properties else None)
            for prop in ["source", "destination"]:
                try:
                    verb_args = verb_args + (CurrentContainerType(properties[prop]),)
                except KeyError:
                    pass

            verb_dictionary[verb] = Verb.create(*verb_args)

        return verb_dictionary
