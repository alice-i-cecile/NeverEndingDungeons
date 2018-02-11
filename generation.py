from typing import Dict, Tuple, List, NewType
import random

Dungeon = List[Room]

#TODO: add a generate_element(element_type) function

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

    for i in range(random.randrange(1,5)):
        new_element = Element(description = str(i))
        room.elements.append(new_element)

    room.challenge = Challenge('Trivial')
    room.safety = Safety('Safe')

    room.flavour = 'A very boring room.'

    room.tags.append('boring')

    return room

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
