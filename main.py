# This is a game in which you are the fire demon calcifer
from world.character import Calcifer
from engine.game import Game
from world.action import UserVerbDictionary
from ui.controller import UIControllerCommandLine
from ui.text.parser import TextParser
from world.location import Location
from world.scene import Scene


def main():
    verbs = UserVerbDictionary.from_yaml("world.resources", "verbs.yaml")
    parser = TextParser(verbs)
    output_controller = UIControllerCommandLine(parser)
    location = Location(Scene("You see a room."), [])
    Game(output_controller, Calcifer(location)).start()


if __name__ == '__main__':
    main()
