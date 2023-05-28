from unittest import TestCase
from unittest.mock import Mock

from calcifer.calcifer import Calcifer
from engine.game import Game
from ui.controller import UIController
from world.scene import Scene


class TestGame(TestCase):
    def test_start_outputs_calcifer_description(self):
        """
        Given a mock description scene for Calcifer, when the start routine
        runs then the scene is shown
        """
        # given
        output_controller = Mock(spec=UIController)

        expected_scene = Mock(spec=Scene)
        expected_scene.text = "Test Calcifer description"
        calcifer = Mock(spec=Calcifer)
        calcifer.description = expected_scene

        # when
        game = Game(output_controller, calcifer)
        game.start()

        # then
        output_controller.show_scene.assert_called_with(expected_scene)