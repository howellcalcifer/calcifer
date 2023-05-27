import dataclasses
from typing import Optional
from unittest import TestCase
from unittest.mock import patch, Mock, call

from ui.actions import UserAction, UserVerb
from ui.controller import UIControllerCommandLine
from ui.scene import Scene
from ui.text.parser import TextParser, InvalidUserActionException


class TestUICommandLineShowScene(TestCase):
    ui = UIControllerCommandLine(parser=Mock(spec=TextParser))

    @patch('builtins.print')
    def test_show_scene_prints(self, mocked_print):
        """given an input scene text, show scene sends it to the command line"""
        input_description = "Test scene description"
        expected_output = input_description
        mock_scene = Mock(spec=Scene)
        mock_scene.text = input_description

        self.ui.show_scene(mock_scene)
        mocked_print.assert_called_with(expected_output)

    @patch('builtins.print')
    def test_show_scene_wraps(self, mocked_print):
        """given a long string, output wraps it before sending to the command line"""
        input_description = "I am Calcifer. I have a thin blue face, a thin blue nose, curly green flames for hair and " \
                            "eyebrows, a purple flaming mouth, and savage teeth. My eyes are orange flames with purple " \
                            "pupils. I do not have any evident lower body."
        expected_output = "I am Calcifer. I have a thin blue face, a thin blue nose, curly green flames\nfor hair and " \
                          "eyebrows, a purple flaming mouth, and savage teeth. My eyes are\norange flames with purple " \
                          "pupils. I do not have any evident lower body."
        mock_scene = Mock(spec=Scene)
        mock_scene.text = input_description

        self.ui.show_scene(mock_scene)
        mocked_print.assert_called_with(expected_output)


@dataclasses.dataclass
class UserInput:
    parser_output: UserAction | InvalidUserActionException
    input: Optional[str] = "User input"


@dataclasses.dataclass
class UserInputCase:
    inputs: list[UserInput]
    expected_action: UserAction


nod_verb = UserVerb(name="nod")
frown_verb = UserVerb(name="frown")
nod_action = UserAction(verb=nod_verb, object=None)
frown_action = UserAction(verb=frown_verb, object=None)


class TestUICommandLineUserAction(TestCase):
    cases = [
        UserInputCase(inputs=[UserInput(input="nod", parser_output=nod_action)], expected_action=nod_action),
        UserInputCase(inputs=[UserInput(input="move", parser_output=InvalidUserActionException("Nope")),
                              UserInput(input="frown", parser_output=frown_action)],
                      expected_action=frown_action),
    ]

    def setUp(self) -> None:
        self.mock_parser = Mock(spec=TextParser)
        self.controller = UIControllerCommandLine(parser=self.mock_parser)

    @patch('builtins.input')
    def test_await_user_action_parses_input(self, mock_input):
        """given a series of user inputs, each one is parsed by the
        text parser"""
        for case in self.cases:
            self.mock_parser.parse_user_action.side_effect = (user_input.parser_output for user_input in case.inputs)

            raw_inputs = [user_input.input for user_input in case.inputs]
            mock_input.side_effect = raw_inputs

            self.controller.await_user_action()
            self.mock_parser.parse_user_action.assert_has_calls([call(i) for i in raw_inputs])

    @patch('builtins.input')
    def test_await_user_action(self, _):  # we don't care about the raw input, we care about the parser output
        """Given a series of user inputs, some of which may be invalid,
        the final parsed action is the one that is returned"""

        for case in self.cases:
            self.mock_parser.parse_user_action.side_effect = (user_input.parser_output for user_input in case.inputs)

            raw_inputs = [user_input.input for user_input in case.inputs]
            test_message = "for inputs " + ", ".join(list(raw_inputs))
            actual_action = self.controller.await_user_action()
            self.assertEqual(case.expected_action, actual_action, msg=test_message)
