from unittest import TestCase
from unittest.mock import Mock

from engine.game import Game
from ui.controllers import InputController
from world.character import Character
from world.item import Item, Inventory
from world.location import Location
from world.scene import Scene
from world.verb import UserAction, UserVerb, VerbType


class TestGame(TestCase):
    def setUp(self) -> None:
        self.input_controller = Mock(spec=InputController)
        self.start_location = Mock(spec=Location)
        self.start_location.scene = Mock(spec=Scene)
        self.start_location.inventory = Mock(spec=Inventory)
        self.calcifer = Mock(spec=Character)
        self.calcifer.description = Mock(spec=Scene)
        self.calcifer.location = self.start_location
        self.calcifer.inventory = Mock(spec=Inventory)
        self.game = Game(self.input_controller, self.calcifer)
        self.look_verb = UserVerb(name="look", type=VerbType.LOOK, description=None)
        self.nod_verb = UserVerb(name="nod", type=VerbType.GESTURE, description=None)
        self.quit_verb = UserVerb(name="quit", type=VerbType.QUIT, description=None)
        self.take_verb = UserVerb(name="take", type=VerbType.INVENTORY, description=None)
        self.bob_verb = UserVerb(name="bob", type=VerbType.GESTURE, description=Scene("You bob around a bit"))
        self.rock_item = Item(name="rock")

    def test_start_outputs_calcifer_description(self):
        """
        Given a mock description scene for Calcifer, when the start routine
        runs then he looks at himself
        """
        # when
        self.input_controller.await_user_action.return_value = UserAction(self.quit_verb, None)
        self.game.start()

        # then
        self.assertEqual(self.calcifer, self.calcifer.looking_at)

    def test_look_updates_to_start_location(self):
        """
        When the user gives a look command after game start, Calcifer looks at the start location
        """
        # when
        self.input_controller.await_user_action.side_effect = [UserAction(self.look_verb, None),
                                                               UserAction(self.quit_verb, None)]
        self.game.start()

        # then
        self.assertEqual(self.start_location, self.calcifer.looking_at)

    def test_nod_updates_gesture(self):
        """
        When the user gives a nod command after game start, Calcifer performs a nod gesture,
        which has a default description
        """
        # given

        # when
        self.input_controller.await_user_action.side_effect = [UserAction(self.nod_verb, None),
                                                               UserAction(self.quit_verb, None)]
        self.game.start()

        # then
        self.assertEqual(Scene("You nod"), self.calcifer.gesture.description)
        self.assertEqual("nod", self.calcifer.gesture.name)

    def test_bob_updates_gesture(self):
        """
        When the user gives a bob command after game start, Calcifer performs a nod gesture,
        which has a bespoke description
        """

        # when
        self.input_controller.await_user_action.side_effect = [UserAction(self.bob_verb, None),
                                                               UserAction(self.quit_verb, None)]
        self.game.start()

        # then
        self.assertEqual(self.bob_verb.description, self.calcifer.gesture.description)
        self.assertEqual("bob", self.calcifer.gesture.name)

    def test_take_rock(self):
        """ when the user gives a take rock command, the rock is added to Calcifer's inventory
        and removed from the location"""
        self.input_controller.await_user_action.side_effect = [UserAction(self.take_verb, self.rock_item),
                                                               UserAction(self.quit_verb, None)]
        self.game.start()
        # then
        self.calcifer.inventory.add.assert_called_with(self.rock_item)
        self.calcifer.location.inventory.remove.assert_called_with(self.rock_item)
