from classes import *
from content import *

from typing import Dict, Tuple, List, NewType
import random

Dungeon = List[Room]

# TODO: add support for subclasses
def generate_element(element_type=None: str,
                     description=None: str,
                     gm_notes=None: str,
                     location=None: Location,
                     size=None: Size,
                     tags=[]: Tags,
                     **kwargs) -> Element:
    """Creates a random element to place in a room.

    Args:
        room: The Room to work on.
        description:

    Returns:
        An Element object with completed attributes.
    """

    if element_type is None:
        element_type <- random.sample('Element',
                                      'Interactable',
                                      'NPC',
                                      'SkillCheck')

    if element_type == 'Element':
        element <- Element()
    else if element_type == 'Interactable':
        element <- Interactable()
        element.interaction_result = 'Nothing'
    else if element_type == 'NPC':
        element <- NPC()
        element.race = 'Human'
        element.disposition = 'Indifferent'
        element.inventory = ['sword']
    else if element_type == 'SkillCheck':
        element <- SkillCheck()
        element.ability = ['Strength']
        element.skill = ['Acrobatics']
        element.difficulty = [10]
        element.success = 'You win'
        element.failure = 'You lose'
    else:
        raise ValueError('Invalid element type')

    element.description = 'A boring piece of furniture.'
    element.gm_notes = 'There\'s very little your players can do with this.'
    element.location = (0,0)
    element.size = 'Medium'
    element.tags = ['boring']

    return element

def populate_room(room: Room,
                  n_elements=None: int,
                  shape=None: List[Position],
                  connection_type=None: str,
                  connection_location=None: int,
                  challenge=None: Challenge,
                  safety=None: Safety,
                  flavour=None: str,
                  tags=[]: Tags) -> Room:
    """Adds content to a room.

    Args:
        room: The Room to work on.

    Returns:
        A Room with completed attributes.
    """
    if shape is None:
        shape = [(0,0), (4,0), (4,4), (0,4)]
    room.shape = shape

    for i in range(room.connections):
        if connection_type is None:
            room.connections[i][2] = random.sample(room_connection_types)
        else:
            room.connections[i][2] = connection_type

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

    if challenge is None:
        challenge = random.sample(valid_challenges)
    room.challenge = challenge
    if safety is None:
        challenge = random.sample(valid_safetys)
    room.safety = safety

    if flavour is None:
        room.flavour = random.sample(room_flavours)
    room.flavour = flavour

    if tags is []:
        tags = random.sample(universal_tags)
    room.tags.append(tags)

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
