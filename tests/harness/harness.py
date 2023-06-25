import abc
from unittest import TestCase
from unittest.mock import Mock

from engine.container_factory import CurrentContainerType
from engine.game import Game
from tests.harness.items import items
from tests.harness.locations import locations
from tests.test_parser import verbs
from world.character import Character
from world.item import Inventory, Item
from world.location import Location, Exit


class TestGameCase(TestCase, abc.ABC):
    def setUp(self, mock_inventory: bool = False) -> None:
        self.verbs = verbs
        self.items = items
        self.locations = locations

        self.game = Mock(spec=Game)
        self.location = self.locations['default']
        self.game.protagonist = Mock(spec=Character)
        self.game.protagonist.location = self.location
        self.visible = {}
        if mock_inventory:
            self.ground = Mock(spec=Inventory)
            self.inventory = Mock(spec=Inventory)
        else:
            self.ground = Inventory()
            self.inventory = Inventory()
        self.exits = {}
        self.game.protagonist.inventory = self.inventory
        self.game.protagonist.location.inventory = self.ground
        self.game.protagonist.location.exits = self.exits
        self.game.container.side_effect = self._mock_create_current_container

    def _mock_create_current_container(self, typ: CurrentContainerType):
        if typ == CurrentContainerType.VISIBLE:
            return self.visible
        if typ == CurrentContainerType.LOCATION_ITEMS:
            return self.ground
        if typ == CurrentContainerType.PROTAGONIST_ITEMS:
            return self.inventory
        if typ == CurrentContainerType.LOCATION_EXITS:
            return self.exits

    def add_to_game(self, ground: Item = None, inventory: Item = None, exit: Exit = None):
        if ground:
            self.ground.add(ground)
            self.visible[ground.name] = ground
        if inventory:
            self.inventory.add(inventory)
            self.visible[inventory.name] = inventory
        if exit:
            self.exits[exit.direction] = exit
            self.visible[exit.direction] = exit

    def clear_game(self):
        self.ground = Inventory()
        self.inventory = Inventory()
        self.exits = {}
        self.visible = {}
