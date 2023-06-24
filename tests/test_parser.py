import dataclasses
from typing import Optional
from unittest import TestCase

from engine.container_factory import CurrentContainerType
from world.item import Item, Inventory
from world.verb import Verb, VerbType, InventoryVerb
from world.mappings import VerbMapping
from ui.text.parser import TextParser, InvalidUserActionException, ParsedResult


@dataclasses.dataclass
class UserInputCase:
    user_input: str
    expect_invalid: bool
    expected_result: Optional[ParsedResult] = None
    expect_invalid_message: Optional[str] = None


nod_verb = Verb(name='nod', type=VerbType.GESTURE, description=None, intransitive=True, transitive=False)
take_verb = InventoryVerb(name='take', type=VerbType.INVENTORY, description=None, transitive=True, intransitive=False,
                          source=CurrentContainerType.LOCATION_ITEMS,
                          destination=CurrentContainerType.PROTAGONIST_ITEMS)
drop_verb = InventoryVerb(name='drop', type=VerbType.INVENTORY, description=None, transitive=True, intransitive=False,
                          source=CurrentContainerType.PROTAGONIST_ITEMS,
                          destination=CurrentContainerType.LOCATION_ITEMS)
look_verb = Verb(name='look', type=VerbType.LOOK, description=None, intransitive=True, transitive=True)
quit_verb = Verb(name='quit', type=VerbType.QUIT, description=None, intransitive=True, transitive=False)
verbs = VerbMapping(
    [('drop', drop_verb), ('nod', nod_verb), ('take', take_verb), ('look', look_verb), ('quit', quit_verb)])
rock_item = Item('rock')
entity_dict = {'rock': rock_item}


class TestTranslate(TestCase):
    def setUp(self) -> None:
        self.inventory = Inventory()
        self.ground = Inventory()
        self.visible = Inventory()
        self.parser = TextParser(verbs)

    def test_translate_user_action(self):
        cases = [UserInputCase(user_input="nod", expect_invalid=False,
                               expected_result=ParsedResult(verb=nod_verb)),
                 UserInputCase(user_input="move", expect_invalid=True),
                 UserInputCase(user_input="take", expect_invalid=True),
                 UserInputCase(user_input="drop rock", expect_invalid=False,
                               expected_result=ParsedResult(verb=drop_verb, object_ref_1="rock")),
                 UserInputCase(user_input="take rock", expect_invalid=False,
                               expected_result=ParsedResult(verb=take_verb, object_ref_1="rock")),
                 UserInputCase(user_input="look rock", expect_invalid=False,
                               expected_result=ParsedResult(verb=look_verb, object_ref_1="rock")),
                 UserInputCase(user_input="look", expect_invalid=False,
                               expected_result=ParsedResult(verb=look_verb)),
                 UserInputCase(user_input="quit rock", expect_invalid=True)]
        self.parser.visible_entities = entity_dict
        for case in cases:
            test_case_message = f"for input '{case.user_input}'"
            if case.expect_invalid:
                with self.assertRaises(InvalidUserActionException, msg=test_case_message):
                    self.parser.parse_user_action(case.user_input)
            else:
                actual_result = self.parser.parse_user_action(case.user_input)
                self.assertEqual(case.expected_result, actual_result, msg=test_case_message)
