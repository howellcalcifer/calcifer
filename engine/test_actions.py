import dataclasses
from unittest import TestCase
from unittest.mock import Mock

from engine.game import Game
from ui.controller import UIController
from world.verb import UserVerbDict, UserVerb, UserAction
from engine.action import UserActionObserver, ActionSceneDict
from world.scene import Scene


@dataclasses.dataclass
class VerbCase:
    resource_name: str
    expected_dict: UserVerbDict


cases = [VerbCase(
    resource_name="verbs_1.yaml",
    expected_dict=UserVerbDict(
        [('smile', UserVerb('smile')),
         ('bow', UserVerb('bow')),
         ('grimace', UserVerb('grimace'))
         ]
    ))]


class TestUserVerbDictionary(TestCase):
    def test_from_yaml(self):
        """ Given a test verb resource, the verbs are loaded into a dict"""
        for case in cases:
            actual_dict = UserVerbDict.from_yaml('world.test_resources', case.resource_name)
            self.assertDictEqual(case.expected_dict, actual_dict)


@dataclasses.dataclass
class SceneCase:
    input_action: UserAction
    expected_scene: Scene


nod_text = "You nod your head"
nod_action = UserAction(UserVerb("nod"), None)
nod_scene = Scene(text=nod_text)
scene_cases = [SceneCase(input_action=nod_action, expected_scene=nod_scene)]


class TestUserActionObserver(TestCase):

    def setUp(self):
        self.game = Mock(spec=Game)
        self.ui_controller = Mock(spec=UIController)
        self.action_scene_dict = ActionSceneDict([(nod_action, nod_scene), ])
        self.observer = UserActionObserver(self.ui_controller, self.action_scene_dict)

    def test_update_shows_scene(self):
        """ Given the observer receives an update with am action that maps to a scene,
         that scene is shown"""
        for case in scene_cases:
            self.game.current_action = case.input_action
            self.observer.update(self.game)
            self.ui_controller.show_scene.assert_called_with(case.expected_scene)
