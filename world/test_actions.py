import dataclasses
from unittest import TestCase

from world.action import UserVerbDictionary, UserVerb


@dataclasses.dataclass
class VerbCase:
    resource_name: str
    expected_dict: UserVerbDictionary


cases = [VerbCase(
    resource_name="verbs_1.yaml",
    expected_dict=UserVerbDictionary(
        [('smile', UserVerb('smile')),
         ('bow', UserVerb('bow')),
         ('grimace', UserVerb('grimace'))
         ]
    ))]


class TestUserVerbDictionary(TestCase):
    def test_from_yaml(self):
        """ Given a test verb resource, the verbs are loaded into a dict"""
        for case in cases:
            actual_dict = UserVerbDictionary.from_yaml('world.test_resources', case.resource_name)
            self.assertDictEqual(case.expected_dict, actual_dict)
