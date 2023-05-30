from pattern.observer import Topic, Observer
from ui.controller import UIController
from world.scene import Scene


class UITopic(Topic):

    def __init__(self):
        super().__init__()
        self.scene: Scene | None = None


class SceneObserver(Observer):

    def __init__(self, ui: UIController):
        self._ui = ui

    def update(self, topic: UITopic) -> None:
        if topic.scene:
            self._ui.show_scene(topic.scene)
        else:
            raise Exception("No scene set for UI topic update")
