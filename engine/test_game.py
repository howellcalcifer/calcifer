from unittest import TestCase
from unittest.mock import Mock, call

from calcifer.calcifer import Calcifer
from engine.game import Game
from ui.controller import UIController
from world.action import UserAction, UserVerb
from world.location import Location
from world.scene import Scene


class TestGame(TestCase):
    def setUp(self) -> None:
        self.ui_controller = Mock(spec=UIController)
        self.calcifer = Mock(spec=Calcifer)
        self.calcifer.description = Mock(spec=Scene)
        self.start_location = Mock(spec=Location)
        self.start_location.scene = Mock(spec=Scene)
        self.game = Game(self.ui_controller, self.calcifer)

    def test_start_outputs_calcifer_description(self):
        """
        Given a mock description scene for Calcifer, when the start routine
        runs then the scene is shown
        """
        # given
        expected_scene = self.calcifer.description

        # when
        self.game.start(self.start_location)

        # then
        self.ui_controller.show_scene.assert_called_with(expected_scene)

    def test_look_shows_location_scene(self):
        """ given a mock start location, when the user looks then the location
        scene is shown"""
        # given
        look_verb = UserVerb(name="look")
        expected_scene = Mock(spec=Scene)
        expected_scene.text = "Test location description"
        self.start_location.scene = expected_scene

        # when
        self.ui_controller.await_user_action.return_value = UserAction(look_verb, None)
        self.game.start(self.start_location)

        # then
        self.ui_controller.show_scene.assert_called_with(expected_scene)

    def test_nod_does_not_show_location_scene(self):
        """ given a mock start location, when the user just nods then the location
        scene is not shown"""
        # given
        nod_verb = UserVerb(name="nod")
        expected_scene = self.start_location.scene

        # when
        self.ui_controller.await_user_action.return_value = UserAction(nod_verb, None)
        self.game.start(self.start_location)

        # then
        assert ((expected_scene,),) not in self.ui_controller.show_scene.call_args_list

    def test_look_nod_and_quit(self):
        look_verb = UserVerb(name="look")
        nod_verb = UserVerb(name="nod")
        quit_verb = UserVerb(name="quit")
        mock_manager = Mock()
        mock_manager.attach_mock(self.ui_controller.show_scene, "show_scene")
        mock_manager.attach_mock(self.ui_controller.show_event, "show_event")

        expected_scene = self.start_location.scene
        expected_event = None  # this needs to be a nod event

        # when
        self.ui_controller.await_user_action.side_effect = [UserAction(look_verb, None), UserAction(nod_verb, None),
                                                            UserAction(quit_verb, None)]
        self.game.start(self.start_location)

        # then
        mock_manager.assert_has_calls([call.show_scene(expected_scene), call.show_event(expected_event)],
                                      any_order=False)
