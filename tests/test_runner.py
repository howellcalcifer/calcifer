from unittest import TestCase
from unittest.mock import patch

from calcifer.runner import main
from world.verb import UserAction, Verb, VerbType


class TestRunner(TestCase):
    @patch('builtins.input')  #
    @patch('calcifer.runner.Character')
    @patch('calcifer.runner.InputControllerCommandLine')
    @patch('calcifer.runner.Game')
    def test_main_starts_game(self, mock_game_class, mock_input_controller_class, mock_calcifer_class,
                              mock_input):
        """
        Running play starts the game engine with the command line UI, Calcifer
        """
        # given
        mock_input.return_value = "quit"
        mock_input_controller = mock_input_controller_class.return_value
        mock_calcifer = mock_calcifer_class.return_value
        mock_game = mock_game_class.return_value

        # when
        main()

        # then
        mock_game_class.assert_called_with(mock_input_controller, mock_calcifer)
        mock_game.start.assert_called_with()

    @patch('builtins.input')
    @patch('calcifer.runner.TextParser')
    @patch('calcifer.runner.InputControllerCommandLine')
    def test_main_loads_ui_with_parser(self, mock_ui_controller_class,
                                       mock_text_parser_class, mock_input):
        """
        Running play loads the command line UI with the text parser
        """
        # given
        mock_input.return_value = "quit"
        mock_text_parser = mock_text_parser_class.return_value
        mock_ui_controller = mock_ui_controller_class.return_value
        mock_ui_controller.await_user_action.return_value = UserAction(
            Verb("quit", VerbType.QUIT, None, transitive=False, intransitive=True), None)

        # when
        main()

        # then
        mock_ui_controller_class.assert_called_with(mock_text_parser)

    @patch('builtins.input')
    @patch('calcifer.runner.TextParser', autospec=True)
    @patch('calcifer.runner.UserVerbDict', autospec=True)
    @patch('calcifer.runner.CurrentContainerFactory', autospec=True)
    def test_main_loads_parser_with_verbs(self,
                                          mock_current_container_factory_class,
                                          mock_user_verb_dictionary_class, mock_text_parser_class, _):
        """
        Running play loads the verb dictionary and container factory into the parser
        """
        # given
        mock_current_container_factory = mock_current_container_factory_class.return_value
        mock_user_verb_dictionary = mock_user_verb_dictionary_class.from_yaml.return_value
        mock_text_parser = mock_text_parser_class.return_value
        mock_text_parser.parse_user_action.return_value = UserAction(
            Verb("quit", VerbType.QUIT, None, transitive=False, intransitive=True), None)

        # when
        main()

        # then
        mock_user_verb_dictionary_class.from_yaml.assert_called_with('data', 'verbs.yaml')
        mock_text_parser_class.assert_called_with(mock_user_verb_dictionary, mock_current_container_factory)
