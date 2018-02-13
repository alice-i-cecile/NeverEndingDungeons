from classes import *

from typing import Dict, Tuple, List, NewType
import random

Dungeon = List[Room]

def generate_element() -> Element:
    """Creates a random element to place in a room.

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

def populate_room(room: Room) -> Room:
    """Adds content to a room.

    Args:
        room: The Room to work on.

    Returns:
        A Room with completed attributes.
    """

    room.shape = [(0,0), (1,0), (1,1), (0,1)]

    for i in range(room.connections):
        room.connections[i][2] = 'BasicConnection'

        # Rooms are connected left to right
        # Ensure that the layout is geometrically possible
        if room.connections[i][1] < room.id:
            room.connections[i][3] = (random.uniform(0,1), 0)
        else:
            room.connections[i][3] = (random.uniform(0,1), 1)

    room.elements = [generate_elements() for _ in range(random.randrange(1,5)]

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
            rooms[i].connections.append((RoomID(i+1), "", (0,0)))
            rooms[i+1].connections.append((RoomID(i), "", (0,0)))

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
