from unittest import TestCase

from engine.container_factory import CurrentContainerFactory, CurrentContainerType
from world.character import Character
from world.item import Inventory, Item
from world.location import Location
from world.scene import Scene


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

