# This is a engine where you are the fire demon calcifer
from calcifer.calcifer import Calcifer
from engine.game import Game
from ui.actions import UserVerb
from ui.controller import UIController, UIControllerCommandLine
from ui.text.parser import TextParser


def play(output_controller: UIController, calcifer: Calcifer):
    Game(output_controller, calcifer).start()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = TextParser(valid_verbs=[UserVerb(name="nod"), UserVerb(name="frown")])
    play(UIControllerCommandLine(parser), Calcifer())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
