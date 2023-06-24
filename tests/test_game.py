from unittest import TestCase
from unittest.mock import Mock

from engine.container_factory import CurrentContainerType
from engine.game import Game
from ui.controllers import InputController
from world.character import Character
from world.item import Item, Inventory
from world.location import Location
from world.scene import Scene
from world.verb import UserAction, Verb, VerbType, InventoryVerb


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
        self.game = Game(self.input_controller)
        self.game.protagonist = self.calcifer
        self.look_verb = Verb(name="look", type=VerbType.LOOK, description=None, transitive=True, intransitive=True)
        self.nod_verb = Verb(name="nod", type=VerbType.GESTURE, description=None, transitive=True, intransitive=False)
        self.quit_verb = Verb(name="quit", type=VerbType.QUIT, description=None, intransitive=True, transitive=False)
        self.take_verb = InventoryVerb(name="take", type=VerbType.INVENTORY, description=None, intransitive=False,
                                       transitive=False, source=CurrentContainerType.LOCATION_ITEMS,
                                       destination=CurrentContainerType.PROTAGONIST_ITEMS)
        self.drop_verb = InventoryVerb(name="drop", type=VerbType.INVENTORY, description=None, intransitive=False,
                                       transitive=False, source=CurrentContainerType.PROTAGONIST_ITEMS,
                                       destination=CurrentContainerType.LOCATION_ITEMS)
        self.bob_verb = Verb(name="bob", type=VerbType.GESTURE, description=Scene("You bob around a bit"),
                             transitive=False, intransitive=True)
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
