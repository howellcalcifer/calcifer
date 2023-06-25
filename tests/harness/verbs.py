from engine.container_factory import CurrentContainerType
from world.scene import Scene
from world.verb import Verb, VerbType, InventoryVerb

verbs = {
    'look': Verb(name="look", type=VerbType.LOOK, description=None, transitive=True, intransitive=True),
    'nod': Verb(name="nod", type=VerbType.GESTURE, description=None, transitive=True, intransitive=False),
    'bow': Verb(name="bow", type=VerbType.GESTURE, description=Scene("You bow gracefully."),
                transitive=True, intransitive=False),
    'quit': Verb(name="quit", type=VerbType.QUIT, description=None, intransitive=True, transitive=False),
    'take': InventoryVerb(name="take", type=VerbType.INVENTORY, description=None, intransitive=False,
                          transitive=False, source=CurrentContainerType.LOCATION_ITEMS,
                          destination=CurrentContainerType.PROTAGONIST_ITEMS),
    'drop': InventoryVerb(name="drop", type=VerbType.INVENTORY, description=None, intransitive=False,
                          transitive=False, source=CurrentContainerType.PROTAGONIST_ITEMS,
                          destination=CurrentContainerType.LOCATION_ITEMS),
    'bob': Verb(name="bob", type=VerbType.GESTURE, description=Scene("You bob around a bit"),
                transitive=False, intransitive=True)
}
