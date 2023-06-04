from unittest import TestCase
from unittest.mock import Mock

from engine.game import Game
from ui.controllers import InputController
from world.character import Character
from world.location import Location
from world.scene import Scene
from world.verb import UserAction, UserVerb, VerbType


class TestGame(TestCase):
    def setUp(self) -> None:
        self.ui_controller = Mock(spec=InputController)
        self.start_location = Mock(spec=Location)
        self.start_location.scene = Mock(spec=Scene)
        self.calcifer = Mock(spec=Character)
        self.calcifer.description = Mock(spec=Scene)
        self.calcifer.location = self.start_location
        self.game = Game(self.ui_controller, self.calcifer)
        self.look_verb = UserVerb(name="look", type=VerbType.LOOK, description=None)
        self.nod_verb = UserVerb(name="nod", type=VerbType.GESTURE, description=None)
        self.quit_verb = UserVerb(name="quit", type=VerbType.QUIT, description=None)
        self.bob_verb = UserVerb(name="bob", type=VerbType.GESTURE, description=Scene("You bob around a bit"))

    def test_start_outputs_calcifer_description(self):
        """
        Given a mock description scene for Calcifer, when the start routine
        runs then he looks at himself
        """
        # when
        self.ui_controller.await_user_action.return_value = UserAction(self.quit_verb, None)
        self.game.start()

        # then
        self.assertEqual(self.calcifer, self.calcifer.looking_at)

    def test_look_updates_to_start_location(self):
        """
        Given a mock description scene for Calcifer, when the start routine
        runs then he looks at himself
        """
        # when
        self.ui_controller.await_user_action.side_effect = [UserAction(self.look_verb, None),
                                                            UserAction(self.quit_verb, None)]
        self.game.start()

        # then
        self.assertEqual(self.start_location, self.calcifer.looking_at)

    def test_nod_updates_gesture(self):
        """
        Given a mock description scene for Calcifer, when the start routine
        runs then he looks at himself
        """
        # given
        expected_scene = self.calcifer.description

        # when
        self.ui_controller.await_user_action.side_effect = [UserAction(self.nod_verb, None),
                                                            UserAction(self.quit_verb, None)]
        self.game.start()

        # then
        self.assertEqual(Scene("You nod"), self.calcifer.gesture.description)
        self.assertEqual("nod", self.calcifer.gesture.name)

    def test_bob_updates_gesture(self):
        """
        Given a mock description scene for Calcifer, when the start routine
        runs then he looks at himself
        """

        # when
        self.ui_controller.await_user_action.side_effect = [UserAction(self.bob_verb, None),
                                                            UserAction(self.quit_verb, None)]
        self.game.start()

        # then
        self.assertEqual(self.bob_verb.description, self.calcifer.gesture.description)
        self.assertEqual("bob", self.calcifer.gesture.name)
