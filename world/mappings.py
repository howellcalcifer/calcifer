from __future__ import annotations

from importlib.resources import files
from typing import Any

from yaml import load, Loader

from engine.container_factory import CurrentContainerType
from world.character import Character
from world.item import Inventory, Item
from world.location import Direction, Location, Exit
from world.scene import Scene
from world.verb import Verb, VerbType


class LocationMapping(dict[str, Location]):

    @classmethod
    def from_yaml(cls, package: str, resource: str, items: ItemMapping,
                  characters: CharacterMapping) -> LocationMapping:
        with (files(package) / resource).open('r') as text_io:
            raw_struct = load(text_io, Loader)
        mapping = cls()
        for name, properties in raw_struct.items():
            inventory = cls.load_inventory(properties, items)
            description = Scene(properties.get('description', ''))
            mapping[name] = Location(name, inventory, description)
            cls.set_character_locations(properties, characters, mapping[name])
        for name, properties in raw_struct.items():
            mapping[name].exits = cls.load_exits(properties, mapping)
        return mapping

    @staticmethod
    def load_inventory(yaml_character: dict[str, Any], items: ItemMapping) -> Inventory:
        inventory = Inventory()
        if 'inventory' in yaml_character:
            for item_name in yaml_character['inventory']:
                inventory.add(items[item_name])
        return inventory

    @staticmethod
    def load_exits(yaml_location: dict[str, Any], locations: LocationMapping) -> dict[str, Exit]:
        exits = {}
        if 'exits' in yaml_location:
            for exit in yaml_location['exits']:
                direction = Direction(exit['direction'])
                exits[direction.value] = Exit(direction=direction, leads_to=locations[exit['location']])
        return exits

    @staticmethod
    def set_character_locations(yaml_location: dict[str, Any], characters: CharacterMapping,
                                 location: Location) -> None:
        if 'characters' in yaml_location:
            for char_name in yaml_location['characters']:
                characters[char_name].location = location


class CharacterMapping(dict[str, Character]):

    @classmethod
    def from_yaml(cls, package: str, resource: str, items: ItemMapping) -> CharacterMapping:
        with (files(package) / resource).open('r') as text_io:
            raw_struct = load(text_io, Loader)
        mapping = cls()
        for name, properties in raw_struct.items():
            inventory = cls.load_inventory(properties, items)
            description = Scene(properties['description']) if 'description' in properties else None
            mapping[name] = Character(name, inventory, display_name=properties.get('display_name'),
                                      description=description)
        return mapping

    @staticmethod
    def load_inventory(yaml_character: dict[str, Any], items: ItemMapping) -> Inventory:
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
            description = Scene(properties['description']) if 'description' in properties else None
            item_mapping[name] = Item(name, description=description, display_name=properties.get('display_name'))
        return item_mapping


class VerbMapping(dict[str, Verb]):
    @classmethod
    def from_yaml(cls, package: str, resource: str) -> VerbMapping:
        with (files(package) / resource).open('r') as text_io:
            raw_struct = load(text_io, Loader)
        verb_dictionary = VerbMapping()

        for verb, properties in raw_struct.items():
            verb_type = VerbType(properties["type"])
            description = Scene(properties["description"]) if "description" in properties else Scene(f"You {verb}.")
            transitive = properties.get("transitive")
            intransitive = properties.get("intransitive")
            if verb_type == VerbType.INVENTORY:
                verb_dictionary[verb] = Verb.create(
                    verb, verb_type, description, transitive, intransitive,
                    CurrentContainerType(properties["source"]),
                    CurrentContainerType(properties["destination"]),
                )
            else:
                verb_dictionary[verb] = Verb.create(verb, verb_type, description, transitive, intransitive)

        return verb_dictionary
