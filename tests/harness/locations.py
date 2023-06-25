from world.item import Inventory
from world.location import Location
from world.scene import Scene

locations = {
    'default': Location("default place", Inventory(), Scene("A default location")),
    'east_place': Location("east place", Inventory(), Scene("A place in the east"))
}