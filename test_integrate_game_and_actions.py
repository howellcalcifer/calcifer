from unittest import TestCase
from unittest.mock import Mock, call

from engine.game import Game
from ui.controller import UIController
from world.action import UserAction, UserVerb, ActionSceneDict
from world.character import Calcifer
from world.event.action import UserActionObserver
from world.location import Location
from world.scene import Scene


class TestIntegrateGameActions(TestCase):

    def setUp(self) -> None:
        self.ui_controller = Mock(spec=UIController)

        self.start_location = Mock(spec=Location)
        self.start_location.scene = Mock(spec=Scene)

        self.calcifer = Mock(spec=Calcifer)
        self.calcifer.description = Mock(spec=Scene)
        self.calcifer.location = self.start_location

        self.scene_dict = ActionSceneDict()

        self.game = Game(self.ui_controller, self.calcifer)
        self.action_observer = UserActionObserver(self.ui_controller, self.scene_dict)
        self.game.subscribe(self.action_observer)

        self.look_verb = UserVerb(name="look")
        self.nod_verb = UserVerb(name="nod")
        self.quit_verb = UserVerb(name="quit")

    def test_look_nod_and_quit(self):
        mock_manager = Mock()
        mock_manager.attach_mock(self.ui_controller.show_scene, "show_scene")
        mock_manager.attach_mock(self.ui_controller.await_user_action, "await_user_action")
        nod_action = UserAction(self.nod_verb, None)
        nod_scene = Scene("You nod a bit.")

        # when
        self.scene_dict[nod_action] = nod_scene
        self.ui_controller.await_user_action.side_effect = [UserAction(self.look_verb, None),
                                                            UserAction(self.nod_verb, None),
                                                            UserAction(self.quit_verb, None)]
        self.game.start()

        # then
        mock_manager.assert_has_calls(
            [call.show_scene(self.calcifer.description), call.await_user_action(),
             call.show_scene(self.start_location.scene),
             call.await_user_action(), call.show_scene(nod_scene), call.await_user_action()],
            any_order=False)

    def test_look_shows_location_scene(self):
        """ given a mock start location, when the user looks then the location
        scene is shown"""
        # given
        UserVerb(name="look")
        expected_scene = Mock(spec=Scene)
        expected_scene.text = "Test location description"
        self.start_location.scene = expected_scene

        # when
        self.ui_controller.await_user_action.side_effect = [UserAction(self.look_verb, None),
                                                            UserAction(self.quit_verb, None)]
        self.game.start()

        # then
        self.ui_controller.show_scene.assert_called_with(expected_scene)

    def test_nod_does_not_show_location_scene(self):
        """ given a mock start location, when the user just nods then the location
        scene is not shown"""
        # given
        expected_scene = self.start_location.scene

        # when
        self.ui_controller.await_user_action.side_effect = [UserAction(self.nod_verb, None),
                                                            UserAction(self.quit_verb, None)]
        self.game.start()

        # then
        assert ((expected_scene,),) not in self.ui_controller.show_scene.call_args_list

