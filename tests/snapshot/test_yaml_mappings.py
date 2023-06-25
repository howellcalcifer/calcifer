import yaml

from world.mappings import LocationMapping, CharacterMapping, ItemMapping, VerbMapping


def test_verb_dict_from_yaml(snapshot):
    actual_dict = VerbMapping.from_yaml("data.test", "verbs.yaml")
    snapshot.assert_match(yaml.dump(actual_dict), 'verb_dict.yaml')


def test_item_mapping_from_yaml(snapshot):
    actual_mapping = ItemMapping.from_yaml("data.test", "items.yaml")
    snapshot.assert_match(yaml.dump(actual_mapping), 'item_mapping.yaml')


def test_character_mapping_from_yaml(snapshot):
    item_mapping = ItemMapping.from_yaml("data.test", "items.yaml")
    actual_mapping = CharacterMapping.from_yaml("data.test", "characters.yaml", item_mapping)
    snapshot.assert_match(yaml.dump(actual_mapping), 'character_mapping.yaml')


def test_location_mapping_from_yaml(snapshot):
    item_mapping = ItemMapping.from_yaml("data.test", "items.yaml")
    character_mapping = CharacterMapping.from_yaml("data.test", "characters.yaml", item_mapping)
    location_mapping = LocationMapping.from_yaml("data.test", "locations.yaml", item_mapping, character_mapping)
    snapshot.assert_match(yaml.dump(location_mapping), 'location_mapping.yaml')
    snapshot.assert_match(yaml.dump(item_mapping), 'item_mapping.yaml')
    snapshot.assert_match(yaml.dump(character_mapping), 'character_mapping.yaml')
