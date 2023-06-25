import dataclasses
from typing import Optional
from unittest import TestCase
from unittest.mock import patch, Mock, call

from engine.container_factory import CurrentContainerType
from engine.game import Game
from ui.controllers import OutputControllerCommandLine, InputControllerCommandLine, OutputException
from ui.text.parser import InvalidUserActionException
from world.character import Character
from world.item import Inventory, Item
from world.location import Exit, Location
from world.scene import Scene
from world.verb import Verb, VerbType, InventoryVerb
from engine.action import UserAction, UnresolvedAction


class TestOutputControllerCommandLine(TestCase):
    ui = OutputControllerCommandLine()

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

    def test_show_no_scene_throws(self):
        self.assertRaises(OutputException, self.ui.show_scene, None)

    def test_show_scene_without_text_throws(self):
        self.assertRaises(OutputException, self.ui.show_scene, Scene(None))

    @patch('builtins.print')
    def test_show_scene_preserves_newline(self, mocked_print):
        """ wrapping doesn't lose existing new lines"""
        input_description = "This is a line.\n\nThis is another line."
        expected_output = "This is a line.\n\nThis is another line."
        mock_scene = Mock(spec=Scene)
        mock_scene.text = input_description
        self.ui.show_scene(mock_scene)
        mocked_print.assert_called_with(expected_output)


@dataclasses.dataclass
class UserInput:
    parser_output: UnresolvedAction | InvalidUserActionException
    input: Optional[str] = "User input"


@dataclasses.dataclass
class UserInputCase:
    inputs: list[UserInput]
    expected_action: UserAction


nod_verb = Verb(name="nod", type=VerbType.GESTURE, description=None, intransitive=True, transitive=False)
frown_verb = Verb(name="frown", type=VerbType.GESTURE, description=None, intransitive=True, transitive=False)
take_verb = InventoryVerb(name="take", type=VerbType.INVENTORY, description=None, intransitive=True, transitive=False,
                          source=CurrentContainerType.LOCATION_ITEMS,
                          destination=CurrentContainerType.PROTAGONIST_ITEMS)
drop_verb = InventoryVerb(name="drop", type=VerbType.INVENTORY, description=None, intransitive=True, transitive=False,
                          source=CurrentContainerType.PROTAGONIST_ITEMS,
                          destination=CurrentContainerType.LOCATION_ITEMS)
look_verb = Verb(name="look", type=VerbType.LOOK, description=None, intransitive=True, transitive=True)
go_verb = Verb(name="go", type=VerbType.MOVE, description=None, intransitive=False, transitive=True)

parsed_nod = UnresolvedAction(verb=nod_verb, object_ref_1=None)
parsed_frown = UnresolvedAction(verb=frown_verb, object_ref_1=None)
nod_action = UserAction(verb=nod_verb, object=None)
frown_action = UserAction(verb=frown_verb, object=None)

parsed_look_rock = UnresolvedAction(verb=look_verb, object_ref_1="rock")
parsed_look_sock = UnresolvedAction(verb=look_verb, object_ref_1="sock")

rock_item = Item('rock')
sock_item = Item('sock')

parsed_go = UnresolvedAction(verb=go_verb, object_ref_1="east")
east_place = Location("east_place", Inventory(), Scene("east place"))
east_exit = Exit(direction="east", leads_to=east_place)


class TestInputCommandLineUserAction(TestCase):
    cases = [
        UserInputCase(inputs=[UserInput(input="nod", parser_output=parsed_nod)], expected_action=parsed_nod),
        UserInputCase(inputs=[UserInput(input="move", parser_output=InvalidUserActionException("Nope")),
                              UserInput(input="frown", parser_output=parsed_frown)],
                      expected_action=parsed_frown),
    ]

    @patch('ui.controllers.TextParser')
    def setUp(self, mock_text_parser_class) -> None:
        verbs = {'nod': nod_verb, 'frown': frown_verb, 'take': take_verb}
        self.game = Mock(Game)
        self.location = Location("here", Inventory(), Scene("it is here"))
        self.game.protagonist = Mock(Character)
        self.game.protagonist.location = self.location
        self.controller = InputControllerCommandLine(verbs, self.game)
        self.mock_parser = mock_text_parser_class.return_value
        self.inventory = Inventory()
        self.ground = Inventory()
        self.visible = {}
        self.game.container.side_effect = self._mock_create_current_container
        self.exits = {}

    def _mock_create_current_container(self, typ: CurrentContainerType):
        if typ == CurrentContainerType.VISIBLE:
            return self.visible
        if typ == CurrentContainerType.LOCATION_ITEMS:
            return self.ground
        if typ == CurrentContainerType.PROTAGONIST_ITEMS:
            return self.inventory
        if typ == CurrentContainerType.LOCATION_EXITS:
            return self.exits

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
            self.controller.await_user_action()
            self.assertEqual(case.expected_action, self.controller.action, msg=test_message)

