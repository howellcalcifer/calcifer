from pattern.observer import Observer
from ui.controllers import OutputController
from world.item import Inventory
from world.scene import Scene


class InventoryOutputObserver(Observer):

    def __init__(self, output_controller: OutputController):
        self.output = output_controller

    def update(self, inventory: Inventory) -> None:
        if inventory.item_incoming:
            self.output.show_scene(Scene(f"You take the {inventory.item_incoming.name}."))
        if inventory.item_outgoing:
            self.output.show_scene(Scene(f"You drop the {inventory.item_outgoing.name}."))
