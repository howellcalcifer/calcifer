from unittest import TestCase
from unittest.mock import Mock

from engine.inventory_output_observer import InventoryOutputObserver
from ui.controllers import OutputController
from world.item import Inventory, Item
from world.scene import Scene


class TestInventoryOutput(TestCase):
    def setUp(self) -> None:
        self.output_controller = Mock(spec=OutputController)

        self.inventory = Inventory()
        self.output_observer = InventoryOutputObserver(self.output_controller)
        self.inventory.subscribe(self.output_observer)
        self.rock = Item("rock", Scene("This is a rock"))

    def test_take_rock(self):
        self.inventory.add(self.rock)
        self.assertEqual(self.output_controller.show_scene.call_count, 1)
        take_rock_scene = Scene("You take the rock")
        self.output_controller.show_scene.assert_called_with(take_rock_scene)
