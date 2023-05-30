from unittest import TestCase
from unittest.mock import Mock

from engine.game import Game
from ui.controller import UIController
from world.action import UserAction, UserVerb
from world.character import Calcifer
from world.location import Location
from world.scene import Scene


class TestGame(TestCase):
    def setUp(self) -> None:
        self.ui_controller = Mock(spec=UIController)
        self.start_location = Mock(spec=Location)
        self.start_location.scene = Mock(spec=Scene)
        self.calcifer = Mock(spec=Calcifer)
        self.calcifer.description = Mock(spec=Scene)
        self.calcifer.location = self.start_location
        self.game = Game(self.ui_controller, self.calcifer)
        self.look_verb = UserVerb(name="look")
        self.nod_verb = UserVerb(name="nod")
        self.quit_verb = UserVerb(name="quit")

    def test_start_outputs_calcifer_description(self):
        """
        Given a mock description scene for Calcifer, when the start routine
        runs then the scene is shown
        """
        # given
        expected_scene = self.calcifer.description

        # when
        self.ui_controller.await_user_action.return_value = UserAction(self.quit_verb, None)
        self.game.start()

        # then
        self.ui_controller.show_scene.assert_called_with(expected_scene)
