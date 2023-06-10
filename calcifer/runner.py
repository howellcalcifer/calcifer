# This is a game in which you are the fire demon calcifer
from engine.game import Game
from engine.inventory_output_observer import InventoryOutputObserver
from ui.controllers import OutputControllerCommandLine, InputControllerCommandLine
from ui.text.parser import TextParser
from world.item import Item, Inventory
from world.verb import UserVerbDict
from world.character import Character
from engine.protagonist_output_observer import ProtagonistOutputObserver
from world.location import Location
from world.scene import Scene


def main():
    verbs = UserVerbDict.from_yaml("data", "verbs.yaml")
    output_controller = OutputControllerCommandLine()

    print("Loading action observers")
    protagonist_observer = ProtagonistOutputObserver(output_controller)
    inventory_observer = InventoryOutputObserver(output_controller)

    print("Loading Calcifer")
    location_items = Inventory()
    location_items.add(Item("rock"))
    location = Location("room",  location_items, Scene("You see a room."),)
    inventory = Inventory()
    inventory.subscribe(observer=inventory_observer)
    calcifer = Character("Calcifer", inventory)
    calcifer.description = Scene(
        "You are Calcifer. You have a thin blue face, a thin blue nose, curly green flames for hair"
        "and eyebrows, a purple flaming mouth, and savage teeth. Your eyes are orange flames with"
        "purple pupils. You do not have any evident lower body.")
    calcifer.location = location
    calcifer.subscribe(observer=protagonist_observer)

    print("Loading input controller")
    parser = TextParser(verbs, location)
    input_controller = InputControllerCommandLine(parser)

    print("Starting game")
    game = Game(input_controller, calcifer)
    game.start()
l