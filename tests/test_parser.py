import dataclasses
from typing import Optional
from unittest import TestCase

from world.item import Item
from world.verb import UserAction, UserVerb, UserVerbDict, VerbType
from ui.text.parser import TextParser, InvalidUserActionException


@dataclasses.dataclass
class UserInputCase:
    user_input: str
    expect_invalid: bool
    expected_action: Optional[UserAction] = None
    expect_invalid_message: Optional[str] = None


nod_verb = UserVerb(name='nod', type=VerbType.GESTURE, description=None, intransitive=True)
take_verb = UserVerb(name='take', type=VerbType.INVENTORY, description=None)
look_verb = UserVerb(name='look', type=VerbType.LOOK, intransitive=True, transitive=True)
verbs = UserVerbDict([('nod', nod_verb), ('take', take_verb), ('look', look_verb)])
rock_item = Item('rock')
entity_dict = {'rock': rock_item}


class TestTranslate(TestCase):
    parser = TextParser(verbs)

    def test_translate_user_action(self):
        cases = [UserInputCase(user_input="nod", expect_invalid=False,
                               expected_action=UserAction(verb=nod_verb, object=None)),
                 UserInputCase(user_input="move", expect_invalid=True),
                 UserInputCase(user_input="take", expect_invalid=True),
                 UserInputCase(user_input="take rock", expect_invalid=False,
                               expected_action=UserAction(verb=take_verb, object=rock_item)),
                 UserInputCase(user_input="look rock", expect_invalid=False,
                               expected_action=UserAction(verb=look_verb, object=rock_item)),
                 UserInputCase(user_input="look", expect_invalid=False,
                               expected_action=UserAction(verb=look_verb))]
        self.parser.visible_entities = entity_dict
        for case in cases:
            test_case_message = f"for input {case.user_input}"
            if case.expect_invalid:
                with self.assertRaises(InvalidUserActionException, msg=test_case_message):
                    self.parser.parse_user_action(case.user_input)
            else:
                actual_action = self.parser.parse_user_action(case.user_input)
                self.assertEqual(case.expected_action, actual_action, msg=test_case_message)
