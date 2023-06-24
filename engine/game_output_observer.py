from engine.game import Game
from pattern.observer import Observer
from ui.controllers import OutputController
from world.scene import Scene


class GameOutputObserver(Observer):

    def __init__(self, output_controller: OutputController):
        self.output = output_controller

    def update(self, game: Game) -> None:
        if game.changed_observed_attribute == 'running':
            if game.running:
                self.output.show_scene(game.protagonist.description)
            else:
                self.output.show_scene(Scene("Goodbye for now."))
