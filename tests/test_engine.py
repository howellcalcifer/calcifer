import dataclasses
from unittest import TestCase
from unittest.mock import Mock, call, patch

from engine.action_resolver import ActionResolver, InvalidUnresolvedAction
from engine.container_factory import CurrentContainerFactory, CurrentContainerType
from engine.game import Game
from engine.game_output_observer import GameOutputObserver
from engine.input_game_observer import InputGameObserver
from tests.harness.harness import TestGameCase
from tests.harness.verbs import verbs
from ui.controllers import InputController, OutputController
from world.character import Character
from world.item import Inventory, Item
from world.location import Location, Exit
from world.scene import Scene
from world.verb import Verb, VerbType, InventoryVerb
from engine.action import UserAction, UnresolvedAction


class TestCurrentContainers(TestCase):
    container_factory = CurrentContainerFactory()

    def setUp(self) -> None:
        self.inventory = Inventory()
        self.ground = Inventory()
        self.protagonist = Character('bob', self.inventory)
        self.location = Location('place', inventory=self.ground, description_init=Scene("This is a place"))
        self.protagonist.location = self.location
        self.container_factory = CurrentContainerFactory()
        self.container_factory.protagonist = self.protagonist
        self.container_factory.location = self.location

    def test_container_manager_inventory_contains(self):
        self.inventory.add(Item("rock"))
        container = self.container_factory.create(CurrentContainerType.PROTAGONIST_ITEMS)
        self.assertTrue("rock" in container)
        self.assertFalse("sock" in container)

    def test_container_location_contains(self):
        self.ground.add(Item("sock"))
        container = self.container_factory.create(CurrentContainerType.LOCATION_ITEMS)
        self.assertTrue("sock" in container)
        self.assertFalse("rock" in container)

    def test_container_visible_contains(self):
        self.ground.add(Item("sock"))
        self.inventory.add(Item("rock"))
        container = self.container_factory.create(CurrentContainerType.VISIBLE)
        self.assertTrue("sock" in container)
        self.assertTrue("rock" in container)
        self.assertFalse("lock" in container)

    def test_container_exits_contains(self):
        self.location.exits['east'] = Exit('east', Location('east_place', inventory=Inventory(),
                                                            description_init=Scene("East place")))
        container = self.container_factory.create(CurrentContainerType.LOCATION_EXITS)
        self.assertTrue("east" in container)
        self.assertFalse("west" in container)


@dataclasses.dataclass
class ActionToSceneCase:
    action: UserAction
    scenes: list[Scene]


@dataclasses.dataclass
class ResolveActionCase:
    input_unresolved: UnresolvedAction
    game_context: dict
    expected_resolved: UserAction


@dataclasses.dataclass
class RejectActionCase:
    input_unresolved: UnresolvedAction
    game_context: dict
    expected_reject_message: str


class TestActionResolver(TestGameCase):

    def setUp(self) -> None:
        super().setUp(mock_inventory=False)
        self.resolver = ActionResolver(self.game)

    def test_resolve_actions(self):
        cases = [
            ResolveActionCase(input_unresolved=UnresolvedAction(self.verbs['nod']),
                              game_context={},
                              expected_resolved=UserAction(self.verbs['nod'])),
            ResolveActionCase(input_unresolved=UnresolvedAction(self.verbs['look']),
                              game_context={},
                              expected_resolved=UserAction(self.verbs['look'], self.location)),
            ResolveActionCase(input_unresolved=UnresolvedAction(self.verbs['look'], 'rock'),
                              game_context={'ground': self.items['rock']},
                              expected_resolved=UserAction(self.verbs['look'], self.items['rock'])),
            ResolveActionCase(input_unresolved=UnresolvedAction(self.verbs['take'], 'rock'),
                              game_context={'ground': self.items['rock']},
                              expected_resolved=UserAction(self.verbs['take'], self.items['rock'])),
            ResolveActionCase(input_unresolved=UnresolvedAction(self.verbs['go'], 'east'),
                              game_context={'exit': Exit("east", self.locations['east_place'])},
                              expected_resolved=UserAction(self.verbs['go'],
                                                           Exit("east", self.locations['east_place']))),
        ]
        for case in cases:
            self.add_to_game(**case.game_context)
            actual_action = self.resolver.resolve(case.input_unresolved)
            self.assertEqual(case.expected_resolved, actual_action)

    def test_reject_actions(self):
        cases = [
            RejectActionCase(input_unresolved=UnresolvedAction(self.verbs['take'], "east"),
                             game_context={'exit': Exit("east", self.locations['east_place'])},
                             expected_reject_message="You can't take that."),
            RejectActionCase(input_unresolved=UnresolvedAction(self.verbs['go'], "rock"),
                             game_context={'ground': self.items['rock']},
                             expected_reject_message="You can't go there."),
            RejectActionCase(input_unresolved=UnresolvedAction(self.verbs['look'], "rock"),
                             game_context={},
                             expected_reject_message="You can't see any rock."),
            RejectActionCase(input_unresolved=UnresolvedAction(self.verbs['take'], "rock"),
                             game_context={'inventory': self.items['rock']},
                             expected_reject_message="You can't take that."),

        ]
        for case in cases:
            self.clear_game()
            self.add_to_game(**case.game_context)
            with self.assertRaises(InvalidUnresolvedAction) as context:
                self.resolver.resolve(case.input_unresolved)
            self.assertEqual(case.expected_reject_message, str(context.exception))


class TestInputGameObserver(TestGameCase):

    @patch('engine.input_game_observer.ActionResolver')
    def setUp(self, mock_action_resolver_class) -> None:
        super().setUp(mock_inventory=True)
        self.game.running = True
        self.controller = Mock(InputController)
        self.observer = InputGameObserver(self.game)
        self.mock_action_resolver = mock_action_resolver_class.return_value
        self.resolve = self.mock_action_resolver.resolve

    def test_resolves_controller_action(self):
        input_action = UnresolvedAction(self.verbs['nod'])
        self.controller.action = input_action
        self.observer.update(self.controller)
        self.resolve.assert_called_with(input_action)

    def test_quits_on_quit_action(self):
        self.resolve.return_value = UserAction(self.verbs['quit'])
        self.observer.update(self.controller)
        self.assertFalse(self.game.running)

    def test_takes_on_take_action(self):
        self.resolve.return_value = UserAction(self.verbs['take'], self.items['rock'])
        self.observer.update(self.controller)
        self.game.protagonist.inventory.add.assert_called_with(self.items['rock'])
        self.game.protagonist.location.inventory.remove.assert_called_with(self.items['rock'])

    def test_drops_on_drop_action(self):
        self.resolve.return_value = UserAction(self.verbs['drop'], self.items['rock'])
        self.observer.update(self.controller)
        self.game.protagonist.inventory.remove.assert_called_with(self.items['rock'])
        self.game.protagonist.location.inventory.add.assert_called_with(self.items['rock'])

    def test_move_on_move_action(self):
        east_exit = Exit("east", self.locations['east_place'])
        self.resolve.return_value = UserAction(self.verbs['go'], east_exit)
        self.observer.update(self.controller)
        self.assertEqual(self.game.protagonist.location, self.locations['east_place'])

    def test_publishes_rejected_action(self):
        rejected_action = InvalidUnresolvedAction("A bad thing happened")
        self.resolve.side_effect = rejected_action
        self.observer.update(self.controller)
        self.assertEqual(self.game.latest_rejected_action, rejected_action)

    def test_set_latest_action(self):
        resolved_action = UserAction(self.verbs['drop'], self.items['rock'])
        self.resolve.return_value = resolved_action
        self.observer.update(self.controller)
        self.assertEqual(self.game.latest_action, resolved_action)


class TestGameOutputObserver(TestGameCase):

    def setUp(self) -> None:
        super().setUp(mock_inventory=False)
        self.output = Mock(OutputController)
        self.observer = GameOutputObserver(self.output)

    def test_shows_quit_scene_when_stop_running(self):
        self.game.running = False
        self.game.changed_observed_attribute = 'running'
        self.observer.update(self.game)
        self.output.show_scene.assert_called_with(Scene("Goodbye for now."))

    def test_shows_protagonist_when_start_running(self):
        self.game.running = True
        self.game.changed_observed_attribute = 'running'
        self.game.protagonist = Mock(Character)
        self.game.protagonist.description = Scene("You seem nice.")
        self.observer.update(self.game)
        self.output.show_scene.assert_called_with(Scene("You seem nice."))

    def test_shows_scenes_for_action(self):
        cases = [
            ActionToSceneCase(action=UserAction(self.verbs['look'], self.location), scenes=[self.location.description]),
            ActionToSceneCase(action=UserAction(self.verbs['nod']), scenes=[self.verbs['nod'].description]),
            ActionToSceneCase(action=UserAction(self.verbs['take'], self.items['rock']),
                              scenes=[Scene("You take the rock.")]),
            ActionToSceneCase(action=UserAction(self.verbs['go'], Exit('east', self.locations['east_place'])),
                              scenes=[Scene("You go east.\n"), self.locations['east_place'].description])
        ]
        for case in cases:
            self.game.latest_action = case.action
            self.game.changed_observed_attribute = 'latest_action'
            self.observer.update(self.game)
            self.output.show_scene.assert_has_calls([call(scene) for scene in case.scenes])

    def test_shows_scene_for_rejected_action(self):
        self.game.latest_rejected_action = InvalidUnresolvedAction("That's a fail")
        self.game.changed_observed_attribute = 'latest_rejected_action'
        self.observer.update(self.game)
        self.output.show_scene.assert_called_with(Scene("That's a fail"))
