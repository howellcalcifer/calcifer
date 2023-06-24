# This is a game in which you are the fire demon calcifer
from engine.game import Game
from engine.game_output_observer import GameOutputObserver
from engine.input_game_observer import InputGameObserver
from engine.inventory_output_observer import InventoryOutputObserver
from engine.protagonist_output_observer import ProtagonistOutputObserver
from ui.controllers import OutputControllerCommandLine, InputControllerCommandLine
from world.mappings import ItemMapping, CharacterMapping, LocationMapping, VerbMapping


def main():
    verbs = VerbMapping.from_yaml("data", "verbs.yaml")

    items = ItemMapping.from_yaml("data", "items.yaml")
    characters = CharacterMapping.from_yaml("data", "characters.yaml", items)
    LocationMapping.from_yaml("data", "locations.yaml", items, characters)
    protagonist_name = 'calcifer'
    protagonist = characters[protagonist_name]
    game = Game()
    input_controller = InputControllerCommandLine(verbs, game)
    output_controller = OutputControllerCommandLine()

    protagonist_observer = ProtagonistOutputObserver(output_controller)
    inventory_observer = InventoryOutputObserver(output_controller)
    game_observer = GameOutputObserver(output_controller)
    protagonist.subscribe(observer=protagonist_observer)
    protagonist.inventory.subscribe(observer=inventory_observer)
    game.subscribe(observer=game_observer)

    input_observer = InputGameObserver(game)
    input_controller.subscribe(input_observer)

    game.protagonist = protagonist
    game.running = True
    input_controller.start()