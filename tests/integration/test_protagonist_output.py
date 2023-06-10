from unittest import TestCase
from unittest.mock import Mock, call

from engine.protagonist_output_observer import ProtagonistOutputObserver
from ui.controllers import OutputController
from world.character import Character, Gesture
from world.location import Location
from world.scene import Scene


class TestIntegrateCharacterActions(TestCase):

    def setUp(self) -> None:
        self.output_controller = Mock(spec=OutputController)
        start_location_scene = Mock(spec=Scene)
        start_location_scene.text="Here is the start location"
        self.start_location = Location("Start", [], description_init=start_location_scene)

        self.calcifer_description = "This is Calcifer"
        self.calcifer = Character("Calcifer")
        self.calcifer.location = Scene(self.calcifer_description)

        self.output_observer = ProtagonistOutputObserver(self.output_controller)
        self.calcifer.subscribe(self.output_observer)

    def test_look(self):
        """ Looking shows the start location scene"""
        self.calcifer.looking_at = self.start_location
        self.assertEqual(self.output_controller.show_scene.call_count, 1)
        self.output_controller.show_scene.assert_called_with(self.start_location.description)

    def test_look_and_nod(self):
        """ Looking then nodding shows the start location, then the nod gesture"""
        look_scene = Mock(spec=Scene)
        look_scene.text = "Test location description"
        look_location = Location("start", [], description_init=look_scene)

        nod_scene = Mock(spec=Scene)
        nod_scene.text = "You nod"
        nod_gesture = Gesture("nod", nod_scene)

        self.calcifer.looking_at = look_location
        self.calcifer.gesture = nod_gesture

        self.assertEqual(self.output_controller.show_scene.call_count, 2)
        self.output_controller.show_scene.assert_has_calls([call.show_scene(look_scene), call.show_scene(nod_scene)],
                                                           any_order=False)

    def test_look_twice(self):
        """ Looking twice shows the start location scene twice"""
        look_scene = Mock(spec=Scene)
        look_scene.text = "Test location description"
        look_location = Location("start", [], look_scene)

        self.calcifer.looking_at = look_location
        self.calcifer.looking_at = look_location
        self.assertEqual(self.output_controller.show_scene.call_count, 2)
        self.output_controller.show_scene.assert_has_calls([call.show_scene(look_scene), call.show_scene(look_scene)],
                                                           any_order=False)
