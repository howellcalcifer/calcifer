import yaml

from world.verb import UserVerbDict


def test_verb_dict_from_yaml(snapshot):
    actual_dict = UserVerbDict.from_yaml("data.test", "verbs_1.yaml")
    snapshot.assert_match(yaml.dump(actual_dict), 'verb_dict.yaml')
