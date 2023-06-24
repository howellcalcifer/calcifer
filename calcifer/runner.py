# This is a game in which you are the fire demon calcifer
from engine.game import Game
from engine.inventory_output_observer import InventoryOutputObserver
from engine.protagonist_output_observer import ProtagonistOutputObserver
from ui.controllers import OutputControllerCommandLine, InputControllerCommandLine
from world.mappings import ItemMapping, CharacterMapping, LocationMapping, VerbMapping


def main():
    verbs = VerbMapping.from_yaml("data", "verbs.yaml")

    items = ItemMapping.from_yaml("data", "items.yaml")
    characters = CharacterMapping.from_yaml("data", "characters.yaml", items)
    locations = LocationMapping.from_yaml("data", "locations.yaml", items, characters)
    start_location_name = 'start'
    protagonist_name = 'calcifer'
    protagonist = characters[protagonist_name]

    input_controller = InputControllerCommandLine(verbs)
    game = Game(input_controller)

    output_controller = OutputControllerCommandLine()
    protagonist_observer = ProtagonistOutputObserver(output_controller)
    inventory_observer = InventoryOutputObserver(output_controller)
    protagonist.subscribe(observer=protagonist_observer)
    protagonist.inventory.subscribe(observer=inventory_observer)

    protagonist.location = locations[start_location_name]
    game.protagonist = protagonist
    game.start()
