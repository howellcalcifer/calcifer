import dataclasses
from typing import Optional
from unittest import TestCase

from world.action import UserAction, UserVerb, UserVerbDictionary
from ui.text.parser import TextParser, InvalidUserActionException


@dataclasses.dataclass
class UserInputCase:
    user_input: str
    expect_invalid: bool
    expected_action: Optional[UserAction] = None
    expect_invalid_message: Optional[str] = None


nod_verb = UserVerb(name='nod')
verbs = UserVerbDictionary([('nod', nod_verb)])


class TestTranslate(TestCase):
    parser = TextParser(verbs)

    def test_translate_user_action(self):
        cases = [UserInputCase(user_input="nod", expect_invalid=False,
                               expected_action=UserAction(verb=nod_verb, object=None)),
                 UserInputCase(user_input="move", expect_invalid=True)]
        for case in cases:
            test_case_message = f"for input {case.user_input}"
            if case.expect_invalid:
                with self.assertRaises(InvalidUserActionException, msg=test_case_message):
                    self.parser.parse_user_action(case.user_input)
            else:
                actual_action = self.parser.parse_user_action(case.user_input)
                self.assertEqual(case.expected_action, actual_action, msg=test_case_message)
