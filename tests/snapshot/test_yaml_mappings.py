import yaml

from world.character import CharacterMapping
from world.item import ItemMapping
from world.verb import VerbMapping


def test_verb_dict_from_yaml(snapshot):
    actual_dict = VerbMapping.from_yaml("data.test", "verbs_1.yaml")
    snapshot.assert_match(yaml.dump(actual_dict), 'verb_dict.yaml')


def test_item_mapping_from_yaml(snapshot):
    actual_mapping = ItemMapping.from_yaml("data.test", "items_1.yaml")
    snapshot.assert_match(yaml.dump(actual_mapping), 'item_mapping.yaml')


def test_character_mapping_from_yaml(snapshot):
    item_mapping = ItemMapping.from_yaml("data.test", "items_1.yaml")
    actual_mapping = CharacterMapping.from_yaml("data.test", "characters_1.yaml", item_mapping)
    snapshot.assert_match(yaml.dump(actual_mapping), 'character_mapping.yaml')
