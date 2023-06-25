from engine.game import Game
from pattern.observer import Observer
from ui.controllers import OutputController
from world.scene import Scene
from world.verb import VerbType


class GameOutputObserver(Observer):

    def __init__(self, output_controller: OutputController):
        self.output = output_controller

    def update(self, game: Game) -> None:
        if game.changed_observed_attribute == 'running':
            if game.running:
                self.output.show_scene(game.protagonist.description)
            else:
                self.output.show_scene(Scene("Goodbye for now."))
        if game.changed_observed_attribute == 'latest_action':
            action = game.latest_action
            if action.verb.type == VerbType.LOOK:
                self.output.show_scene(action.object.description)
            elif action.verb.type == VerbType.GESTURE:
                self.output.show_scene(action.verb.description)
            elif action.verb.type == VerbType.INVENTORY:
                self.output.show_scene(Scene(f"You {action.verb.name} the {action.object.name}."))
            elif action.verb.type == VerbType.MOVE:
                self.output.show_scene(Scene(f"You go {action.object.direction}.\n"))
                self.output.show_scene(action.object.leads_to.description)
