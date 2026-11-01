from typing import assert_never

from engine.events import ActionApplied, ActionRejected, GameEvent, GameStarted, GameStopped
from pattern.observer import Observer
from ui.controllers import OutputController
from world.item import Item
from world.location import Exit
from world.scene import Scene
from world.verb import VerbType


class GameOutputObserver(Observer[GameEvent]):

    def __init__(self, output_controller: OutputController):
        self.output = output_controller

    def update(self, event: GameEvent) -> None:
        if isinstance(event, GameStarted):
            self.output.show_scene(event.protagonist.description)
        elif isinstance(event, GameStopped):
            self.output.show_scene(Scene("Goodbye for now."))
        elif isinstance(event, ActionRejected):
            self.output.show_scene(Scene(str(event.error)))
        elif isinstance(event, ActionApplied):
            action = event.action
            if action.verb.type == VerbType.LOOK:
                assert action.object is not None
                self.output.show_scene(action.object.description)
            elif action.verb.type == VerbType.GESTURE:
                self.output.show_scene(action.verb.description)
            elif action.verb.type == VerbType.ITEM_TRANSFER:
                assert isinstance(action.object, Item)
                self.output.show_scene(Scene(f"You {action.verb.name} the {action.object.name}."))
            elif action.verb.type == VerbType.INVENTORY:
                item_names = [str(item) for item in action.inventory or ()]
                if item_names:
                    self.output.show_scene(Scene(f"You are carrying: {', '.join(item_names)}."))
                else:
                    self.output.show_scene(Scene("You are carrying nothing."))
            elif action.verb.type == VerbType.MOVE:
                assert isinstance(action.object, Exit)
                self.output.show_scene(Scene(f"You go {action.object.direction}.\n"))
                self.output.show_scene(action.object.leads_to.description)
            elif action.verb.type == VerbType.MAGIC:
                assert action.verb.description is not None
                self.output.show_scene(action.verb.description)
        else:
            assert_never(event)
