import dataclasses
from typing import Type
from unittest import TestCase

from engine.game import Game
from world.character import Describable, Character, Gesture
from world.item import Item, Inventory
from world.location import Location
from world.scene import Scene
from world.verb import Verb
from world.mappings import VerbMapping


@dataclasses.dataclass
class DescribableTestCase:
    cls: Type
    expected_is_describable: bool


@dataclasses.dataclass
class VerbDictTestCase:
    verb_file: str
    expected_dict: VerbMapping


class TestWorld(TestCase):
    def test_describable_issubclass_behaviour(self):
        cases = [DescribableTestCase(Item, True), DescribableTestCase(Character, True),
                 DescribableTestCase(Location, True),
                 DescribableTestCase(Gesture, True), DescribableTestCase(Verb, True),
                 DescribableTestCase(Game, False)]
        for case in cases:
            actual_is_describable = issubclass(case.cls, Describable)
            self.assertEqual(case.expected_is_describable, actual_is_describable, msg=f"for ${case.cls}")

    def test_location_description(self):
        input_scene = Scene("Here lies a scene, the scene is green")
        inventory = Inventory()
        location = Location("test", inventory, input_scene)
        self.assertEqual(location.description, input_scene)

    def test_location_description_single_item(self):
        input_scene = Scene("A scene.")
        inventory = Inventory()
        inventory.add(Item("rock"))
        location = Location("test", inventory, input_scene)
        self.assertEqual("A scene.\n\nA rock is here.", location.description.text)
