from unittest import TestCase
from unittest.mock import patch

from calcifer.runner import main


class TestRunner(TestCase):
    @patch('builtins.input')
    @patch('calcifer.runner.InputControllerCommandLine')
    @patch('calcifer.runner.Game')
    def test_main_starts_game(self, mock_game_class, mock_input_controller_class, mock_input):
        """
        Running play starts the game engine with the command line UI
        """
        # given
        mock_input.return_value = "quit"
        mock_input_controller = mock_input_controller_class.return_value
        mock_game = mock_game_class.return_value

        # when
        main()

        # then
        mock_game_class.assert_called_with(mock_input_controller)
        mock_game.start.assert_called_with()

    @patch('calcifer.runner.Game')
    @patch('calcifer.runner.InputControllerCommandLine', autospec=True)
    @patch('calcifer.runner.VerbMapping', autospec=True)
    def test_main_loads_parser_with_verbs(self,
                                          mock_verb_mapping_class, mock_input_controller_class, _):
        """
        Running play loads the verb mapping into the input controller
        """
        # given
        mock_verb_mapping = mock_verb_mapping_class.from_yaml.return_value

        # when
        main()

        # then
        mock_verb_mapping_class.from_yaml.assert_called_with('data', 'verbs.yaml')
        mock_input_controller_class.assert_called_with(mock_verb_mapping)
