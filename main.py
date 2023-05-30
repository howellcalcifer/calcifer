# This is a game in which you are the fire demon calcifer
from engine.game import Game
from ui.controller import UIControllerCommandLine
from ui.text.parser import TextParser
from world.verb import UserVerbDict, UserAction
from world.character import Calcifer
from engine.action import UserActionObserver, ActionSceneDict
from world.location import Location
from world.scene import Scene


def main():

    print("Loading UI controller")
    verbs = UserVerbDict.from_yaml("world.resources", "verbs.yaml")
    parser = TextParser(verbs)
    output_controller = UIControllerCommandLine(parser)

    print("Loading action observer")
    scene_dict = ActionSceneDict()
    scene_dict[UserAction(verbs["nod"], None)] = Scene("You nod your head")
    action_observer = UserActionObserver(output_controller, scene_dict)

    print("Loading Calcifer")
    location = Location(Scene("You see a room."), [])
    calcifer = Calcifer(location)

    print("Starting game")
    game = Game(output_controller, calcifer)
    game.subscribe(action_observer)
    game.start()


if __name__ == '__main__':
    main()
