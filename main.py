# This is a game in which you are the fire demon calcifer
from calcifer.calcifer import Calcifer
from engine.game import Game
from world.action import UserVerbDictionary
from ui.controller import UIControllerCommandLine
from ui.text.parser import TextParser


def main():
    verbs = UserVerbDictionary.from_yaml("world.resources", "verbs.yaml")
    parser = TextParser(verbs)
    output_controller = UIControllerCommandLine(parser)
    Game(output_controller, Calcifer()).start()


if __name__ == '__main__':
    main()
