import dataclasses
from typing import Type
from unittest import TestCase

from engine.game import Game
from world.character import Describable, Character, Gesture
from world.item import Item
from world.location import Location
from world.verb import UserVerb


@dataclasses.dataclass
class DescribableTestCase:
    cls: Type
    expected_is_describable: bool


class TestWorld(TestCase):
    def test_describable_issubclass_behaviour(self):
        cases = [DescribableTestCase(Item, True), DescribableTestCase(Character, True), DescribableTestCase(Location, True),
                 DescribableTestCase(Gesture, True), DescribableTestCase(UserVerb, True),
                 DescribableTestCase(Game, False)]
        for case in cases:
            actual_is_describable = issubclass(case.cls, Describable)
            self.assertEqual(case.expected_is_describable, actual_is_describable, msg=f"for ${case.cls}")

