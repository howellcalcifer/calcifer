from unittest import TestCase
from unittest.mock import Mock

from calcifer.calcifer import Calcifer
from engine.game import Game
from ui.controller import UIController
from world.action import UserAction, UserVerb
from world.location import Location
from world.scene import Scene


class TestGame(TestCase):
    def setUp(self) -> None:
        self.output_controller = Mock(spec=UIController)
        self.calcifer = Mock(spec=Calcifer)
        self.start_location = Mock(spec=Location)
        self.game = Game(self.output_controller, self.calcifer)

    def test_start_outputs_calcifer_description(self):
        """
        Given a mock description scene for Calcifer, when the start routine
        runs then the scene is shown
        """
        # given
        expected_scene = Mock(spec=Scene)
        expected_scene.text = "Test Calcifer description"
        self.calcifer.description = expected_scene

        # when
        self.game.start(self.start_location)

        # then
        self.output_controller.show_scene.assert_called_with(expected_scene)

    def test_look_shows_location_scene(self):
        """ given a mock start location, when the user looks then the location
        scene is shown"""
        # given
        look_verb = UserVerb(name="look")
        expected_scene = Mock(spec=Scene)
        expected_scene.text = "Test location description"
        self.start_location.scene = expected_scene

        # when
        self.output_controller.await_user_action.return_value = UserAction(look_verb, None)
        self.game.start(self.start_location)

        # then
        self.output_controller.show_scene.assert_called_with(expected_scene)

    def test_nod_does_not_show_location_scene(self):
        """ given a mock start location, when the user just nods then the location
        scene is not shown"""
        # given
        nod_verb = UserVerb(name="nod")
        expected_scene = Mock(spec=Scene)
        expected_scene.text = "Test location description"
        self.start_location.scene = expected_scene

        # when
        self.output_controller.await_user_action.return_value = UserAction(nod_verb, None)
        self.game.start(self.start_location)

        # then
        assert ((expected_scene,),) not in self.output_controller.show_scene.call_args_list
