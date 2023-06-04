from __future__ import annotations

from pattern.observer import Observer
from ui.controllers import OutputController
from world.character import Character


class ProtagonistOutputObserver(Observer):

    def __init__(self, output_controller: OutputController):
        self.output = output_controller

    def update(self, character: Character) -> None:
        if character.changed_observed_attribute == 'looking_at' and character.looking_at:
            self.output.show_scene(character.looking_at.description)

        if character.changed_observed_attribute == 'gesture' and character.gesture:
            self.output.show_scene(character.gesture.description)