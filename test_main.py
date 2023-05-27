from unittest import TestCase
from unittest.mock import Mock, patch

from calcifer.calcifer import Calcifer
from main import play
from ui.controller import UIController


class TestPlay(TestCase):
    @patch('main.Game')
    def test_play_starts_game(self, mock_game_constructor):
        """
        Running play starts the game engine
        """
        # given
        output_controller = Mock(spec=UIController)
        calcifer = Mock(spec=Calcifer)
        mock_game = mock_game_constructor.return_value

        # when
        play(output_controller=output_controller, calcifer=calcifer)

        # then
        mock_game_constructor.assert_called_with(output_controller, calcifer)
        mock_game.start.assert_called_with()
