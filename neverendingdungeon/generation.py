from classes import *
from content import *

from typing import Dict, Tuple, List, NewType
import random

Dungeon = List[Room]

# TODO: add support for subclasses
def generate_element(element_type=None: str,
                     description_id=None: int,
                     gm_notes_id=None: int,
                     location=None: Location,
                     size=None: int,
                     tags_id=[]: int,
                     **kwargs) -> Element:
    """Creates a random element to place in a room.

    Args:
        room: The Room to work on.
        description_id:

    Returns:
        An Element object with completed attributes.
    """

    element <- Element()
    element.description = 'A boring piece of furniture.'
    element.gm_notes = 'There\'s very little your players can do with this.'
    element.location = (0,0)
    element.size = 'Medium'
    element.tags = ['boring']

    return element

def populate_room(room: Room,
                  n_elements=None: int,
                  shape=None: List[Position],
                  connection_type_id=None: int,
                  connection_location=None: int,
                  challenge=None: Challenge,
                  safety=None: Safety,
                  flavour_id=None: str,
                  tags=[]: Tags) -> Room:
    """Adds content to a room.

    Args:
        room: The Room to work on.

    Returns:
        A Room with completed attributes.
    """

    room.shape = [(0,0), (4,0), (4,4), (0,4)]

    for i in range(room.connections):
        room.connections[i][2] = 'BasicConnection'

        # Rooms are connected left to right
        # Ensure that the layout is geometrically possible
        if room.connections[i][1] < room.id:
            if connection_location is None:
                room.connections[i][3] = (random.randrange(0,4), 0)
            else:
                room.connections[i][3] = (connection_location, 0)
        else:
            if connection_location is None:
                room.connections[i][3] = (random.randrange(0,4), 1)
            else:
                room.connections[i][3] = (connection_location, 1)

    if n_elements is None:
        n_elements = random.randrange(1,5)

    room.elements = [generate_element() for _ in range(n_elements)]

    room.challenge = Challenge('Trivial')
    room.safety = Safety('Safe')

    room.flavour = 'A very boring room.'

    room.tags.append('boring')

    return room

def generate_dungeon_structure(n_rooms: int, layout='linear': string, **kwargs) -> Dungeon:
    """Creates a barren, connected dungeon.

    Args:
        n_rooms: The number of rooms to be created.
        layout: The algorithm used to link rooms into a graph. Defaults to 'linear'.
            Supported options are: 'linear'.
        **kwargs: Additional named parameters to be passed to the layout algorithm.

    Returns:
        A barren dungeon with rooms that only have an ID and connections.
    """

    rooms = [Room(id=i) for i in range(n_rooms)]

    if layout == 'linear':
        for i in range(n_rooms - 1):
            rooms[i].connections.append((RoomID(i+1), '', (0,0)))
            rooms[i+1].connections.append((RoomID(i), '', (0,0)))

    return rooms

def generate_dungeon(n_rooms: int, layout='linear': string, **kwargs) -> Dungeon:
    """Creates a dungeon from scratch.

    Args:
        n_rooms: The number of rooms to be created.
        layout: The algorithm used to link rooms into a graph. Defaults to 'linear'.
            Supported options are: 'linear'.
        **kwargs: Additional named parameters to be passed to the layout algorithm.

    Returns:
        A Dungeon composed of Rooms with completed attributes.
    """

    dungeon = generate_dungeon_structure(n_rooms, layout, **kwargs)
    populated_dungeon = map(populate_room, dungeon)

    return populated_dungeon
