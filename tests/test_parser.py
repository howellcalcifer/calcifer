import dataclasses
from typing import Optional
from unittest import TestCase
from unittest.mock import Mock, patch

from engine.container_factory import CurrentContainerFactory, CurrentContainerType
from world.item import Item, Inventory
from world.verb import UserAction, Verb, VerbMapping, VerbType, InventoryVerb
from ui.text.parser import TextParser, InvalidUserActionException


@dataclasses.dataclass
class UserInputCase:
    user_input: str
    expect_invalid: bool
    expected_action: Optional[UserAction] = None
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
verbs = VerbMapping([('nod', nod_verb), ('take', take_verb), ('look', look_verb), ('quit', quit_verb)])
rock_item = Item('rock')
entity_dict = {'rock': rock_item}


class TestTranslate(TestCase):
    @patch('ui.text.parser.CurrentContainerFactory')
    def setUp(self, container_factory_class) -> None:
        container_factory = container_factory_class.return_value
        self.inventory = Inventory()
        self.ground = Inventory()
        self.visible = Inventory()
        self.visible.add(Item("rock"))
        container_factory.create.side_effect = self._mock_create_current_container
        self.parser = TextParser(verbs)

    def _mock_create_current_container(self, typ: CurrentContainerType):
        if typ == CurrentContainerType.VISIBLE:
            return self.visible
        if typ == CurrentContainerType.LOCATION_ITEMS:
            return self.ground
        if typ == CurrentContainerType.PROTAGONIST_ITEMS:
            return self.inventory

    def test_translate_user_action(self):
        cases = [UserInputCase(user_input="nod", expect_invalid=False,
                               expected_action=UserAction(verb=nod_verb, object=None)),
                 UserInputCase(user_input="move", expect_invalid=True),
                 UserInputCase(user_input="take", expect_invalid=True),
                 UserInputCase(user_input="take rock", expect_invalid=False,
                               expected_action=UserAction(verb=take_verb, object=rock_item, source=self.inventory,
                                                          destination=self.ground)),
                 UserInputCase(user_input="take rock", expect_invalid=False,
                               expected_action=UserAction(verb=take_verb, object=rock_item, source=self.ground,
                                                          destination=self.inventory)),
                 UserInputCase(user_input="look rock", expect_invalid=False,
                               expected_action=UserAction(verb=look_verb, object=rock_item)),
                 UserInputCase(user_input="look", expect_invalid=False,
                               expected_action=UserAction(verb=look_verb)),
                 UserInputCase(user_input="quit rock", expect_invalid=True)]
        self.parser.visible_entities = entity_dict
        for case in cases:
            test_case_message = f"for input '{case.user_input}'"
            if case.expect_invalid:
                with self.assertRaises(InvalidUserActionException, msg=test_case_message):
                    self.parser.parse_user_action(case.user_input)
            else:
                actual_action = self.parser.parse_user_action(case.user_input)
                self.assertEqual(case.expected_action, actual_action, msg=test_case_message)
