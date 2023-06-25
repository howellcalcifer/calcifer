# This is a game in which you are the fire demon calcifer
from engine.game import Game
from engine.game_output_observer import GameOutputObserver
from engine.input_game_observer import InputGameObserver
from ui.controllers import OutputControllerCommandLine, InputControllerCommandLine
from world.mappings import ItemMapping, CharacterMapping, LocationMapping, VerbMapping


def main(data_module: str = 'data'):
    verbs = VerbMapping.from_yaml(data_module, "verbs.yaml")

    items = ItemMapping.from_yaml(data_module, "items.yaml")
    characters = CharacterMapping.from_yaml(data_module, "characters.yaml", items)
    LocationMapping.from_yaml(data_module, "locations.yaml", items, characters)
    protagonist_name = 'calcifer'
    protagonist = characters[protagonist_name]
    game = Game()
    input_controller = InputControllerCommandLine(verbs, game)
    output_controller = OutputControllerCommandLine()

    game_observer = GameOutputObserver(output_controller)
    game.subscribe(observer=game_observer)

    input_observer = InputGameObserver(game)
    input_controller.subscribe(input_observer)

    game.protagonist = protagonist
    game.running = True
    input_controller.start()
