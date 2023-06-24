from unittest import TestCase
from unittest.mock import patch

from calcifer.runner import main


class TestRunner(TestCase):
    @patch('calcifer.runner.Game', autospec=True)
    @patch('calcifer.runner.InputControllerCommandLine', autospec=True)
    @patch('calcifer.runner.VerbMapping', autospec=True)
    def test_main_loads_parser_with_verbs(self,
                                          mock_verb_mapping_class, mock_input_controller_class, mock_game_class):
        """
        Running play loads the verb mapping into the input controller
        """
        # given
        mock_verb_mapping = mock_verb_mapping_class.from_yaml.return_value
        mock_game = mock_game_class.return_value
        mock_game.running = False

        # when
        main()

        # then
        mock_verb_mapping_class.from_yaml.assert_called_with('data', 'verbs.yaml')
        mock_input_controller_class.assert_called_with(mock_verb_mapping, mock_game)
