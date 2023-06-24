from unittest import TestCase
from unittest.mock import Mock

from engine.container_factory import CurrentContainerFactory, CurrentContainerType
from engine.game import Game
from engine.game_output_observer import GameOutputObserver
from engine.input_game_observer import InputGameObserver
from ui.controllers import InputController, OutputController
from world.character import Character
from world.item import Inventory, Item
from world.location import Location
from world.scene import Scene
from world.verb import Verb, VerbType, InventoryVerb, UserAction


class TestCurrentContainers(TestCase):
    container_factory = CurrentContainerFactory()

    def setUp(self) -> None:
        self.inventory = Inventory()
        self.ground = Inventory()
        self.protagonist = Character('bob', self.inventory)
        self.location = Location('place', inventory=self.ground, description_init=Scene("This is a place"))
        self.protagonist.location = self.location
        self.container_factory = CurrentContainerFactory()
        self.container_factory.protagonist = self.protagonist
        self.container_factory.location = self.location

    def test_container_manager_inventory_contains(self):
        self.inventory.add(Item("rock"))
        container = self.container_factory.create(CurrentContainerType.PROTAGONIST_ITEMS)
        self.assertTrue("rock" in container)
        self.assertFalse("sock" in container)

    def test_container_location_contains(self):
        self.ground.add(Item("sock"))
        container = self.container_factory.create(CurrentContainerType.LOCATION_ITEMS)
        self.assertTrue("sock" in container)
        self.assertFalse("rock" in container)

    def test_container_visible_contains(self):
        self.ground.add(Item("sock"))
        self.inventory.add(Item("rock"))
        container = self.container_factory.create(CurrentContainerType.VISIBLE)
        self.assertTrue("sock" in container)
        self.assertTrue("rock" in container)
        self.assertFalse("lock" in container)


class TestInputGameObserver(TestCase):

    def setUp(self) -> None:
        self.start_location = Mock(spec=Location)
        self.start_location.scene = Mock(spec=Scene)
        self.start_location.inventory = Mock(spec=Inventory)
        self.calcifer = Mock(spec=Character)
        self.calcifer.description = Mock(spec=Scene)
        self.calcifer.location = self.start_location
        self.calcifer.inventory = Mock(spec=Inventory)
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
        self.game = Mock(Game)
        self.game.protagonist = self.calcifer
        self.game.running = True
        self.controller = Mock(InputController)
        self.observer = InputGameObserver(self.game)

    def test_quits_on_quit_action(self):
        self.controller.action = UserAction(self.quit_verb)
        self.observer.update(self.controller)
        self.assertFalse(self.game.running)

    def test_takes_on_take_action(self):
        self.controller.action = UserAction(self.take_verb, self.rock_item)
        self.observer.update(self.controller)

        self.game.protagonist.inventory.add.assert_called_with(self.rock_item)
        self.game.protagonist.location.inventory.remove.assert_called_with(self.rock_item)

    def test_drops_on_drop_action(self):
        self.controller.action = UserAction(self.drop_verb, self.rock_item)
        self.observer.update(self.controller)

        self.game.protagonist.inventory.remove.assert_called_with(self.rock_item)
        self.game.protagonist.location.inventory.add.assert_called_with(self.rock_item)

    def test_looks_around_on_intransitive_look_action(self):
        self.controller.action = UserAction(self.look_verb)
        self.observer.update(self.controller)

        self.assertEqual(self.game.protagonist.looking_at, self.game.protagonist.location)

    def test_looks_at_object_on_transitive_look_action(self):
        self.controller.action = UserAction(self.look_verb, self.rock_item)
        self.observer.update(self.controller)

        self.assertEqual(self.game.protagonist.looking_at, self.rock_item)

    def test_nods_on_nod_action(self):
        self.controller.action = UserAction(self.nod_verb)
        self.observer.update(self.controller)
        self.assertEqual(self.game.protagonist.gesture, Scene("You nod."))


class TestGameOutputObserver(TestCase):

    def setUp(self) -> None:
        self.game = Mock(Game)
        self.output = Mock(OutputController)
        self.observer = GameOutputObserver(self.output)

    def test_shows_quit_scene_when_stop_running(self):
        self.game.running = False
        self.game.changed_observed_attribute = 'running'
        self.observer.update(self.game)
        self.output.show_scene.assert_called_with(Scene("Goodbye for now."))

    def test_shows_protagonist_when_start_running(self):
        self.game.running = True
        self.game.changed_observed_attribute = 'running'
        self.game.protagonist = Mock(Character)
        self.game.protagonist.description = Scene("You seem nice.")
        self.observer.update(self.game)
        self.output.show_scene.assert_called_with(Scene("You seem nice."))
