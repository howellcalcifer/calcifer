from __future__ import annotations

from engine.game import Game
from pattern.observer import Observer
from ui.controller import UIController
from world.action import ActionSceneDict, CoreVerbs


class UserActionObserver(Observer):

    def __init__(self, ui_controller: UIController, scenes: ActionSceneDict):
        self._ui_controller = ui_controller
        self._scenes = scenes

    def update(self, game: Game) -> None:
        try:
            self._ui_controller.show_scene(self._scenes[game.current_action])
        except KeyError:
            pass
        if game.current_action.verb.name == CoreVerbs.LOOK.value and game.current_action.object is None:
            self._ui_controller.show_scene(game.current_location.scene)

