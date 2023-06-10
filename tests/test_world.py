import dataclasses
from typing import Type
from unittest import TestCase

from engine.game import Game
from world.character import Describable, Character, Gesture
from world.item import Item
from world.location import Location
from world.scene import Scene
from world.verb import UserVerb, UserVerbDict, VerbType


@dataclasses.dataclass
class DescribableTestCase:
    cls: Type
    expected_is_describable: bool


@dataclasses.dataclass
class VerbDictTestCase:
    verb_file: str
    expected_dict: UserVerbDict


class TestWorld(TestCase):
    def test_describable_issubclass_behaviour(self):
        cases = [DescribableTestCase(Item, True), DescribableTestCase(Character, True),
                 DescribableTestCase(Location, True),
                 DescribableTestCase(Gesture, True), DescribableTestCase(UserVerb, True),
                 DescribableTestCase(Game, False)]
        for case in cases:
            actual_is_describable = issubclass(case.cls, Describable)
            self.assertEqual(case.expected_is_describable, actual_is_describable, msg=f"for ${case.cls}")

    def test_verb_dict_from_yaml(self):
        verb_dict_1 = UserVerbDict()
        verb_dict_1['smile'] = UserVerb('smile', VerbType.GESTURE, None)
        verb_dict_1['bow'] = UserVerb('bow', VerbType.GESTURE, Scene('You bow gracefully'))
        verb_dict_1['sit'] = UserVerb('sit', VerbType.POSTURE, None)
        verb_dict_1['abracadabra'] = UserVerb('abracadabra', VerbType.MAGIC, None)
        verb_dict_1['east'] = UserVerb('east', VerbType.MOVE, None)
        verb_dict_1['take'] = UserVerb('take', VerbType.INVENTORY, None, True)
        verb_dict_1['drop'] = UserVerb('drop', VerbType.INVENTORY, None, True)

        cases = [VerbDictTestCase("verbs_1.yaml", verb_dict_1), ]

        for case in cases:
            actual_dict = UserVerbDict.from_yaml("data.test", case.verb_file)
            self.assertEqual(case.expected_dict, actual_dict, msg=f"for {case.verb_file}")

    def test_location_description(self):
        input_scene = Scene("Here lies a scene, the scene is green")
        location = Location("test", [], input_scene)
        self.assertEqual(location.description, input_scene)

    def test_location_description_single_item(self):
        input_scene = Scene("A scene.")
        location = Location("test", [Item("rock")], input_scene)
        self.assertEqual("A scene.\n\nA rock is here.",location.description.text)
