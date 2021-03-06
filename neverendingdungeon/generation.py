from classes import *
from content import *
import utilities

from typing import Dict, Tuple, List, NewType
import random

Dungeon = List[Room]

# TODO: generalize for nonrectangular Rooms
def place_element(room: Room, size: str = 'Medium'):
    x_coord = [l[0] for l in room.shape]
    y_coord = [l[1] for l in room.shape]

    # Items are placed at the centers of squares but walls are on edges
    x_min, y_min = min(x_coord), min(y_coord)
    x_max, y_max = max(x_coord) - 1, max(y_coord) - 1

    # FIXME: does not work for rooms with dimension 1
    x, y = random.randrange(x_min, x_max), random.randrange(y_min, y_max)
    return (x,y)

def select_elements(room, xp_budget: int, gold_budget: int):

    elements = []

    viable_tags = room.tags + ['neutral']
    viable_elements = element_df[[utilities.filter_by_tags(r, viable_tags) for r in element_df.tags]]

    # TODO: switch to a nonconvex optimization approach
    current_xp = 0
    while current_xp < xp_budget and len(elements) < 5:

        viable_elements = viable_elements.query(f'xp <= {xp_budget - current_xp}')

        e_series =  viable_elements.loc[random.choice(viable_elements.index), ]
        new_element = utilities.import_element(e_series)

        new_element.location = place_element(room, new_element.size)
        elements.append(new_element)

        current_xp += new_element.xp

    current_gold = sum(e.gold for e in elements)
    if current_gold < gold_budget:

        treasure_elements = element_df.query('element_type == "Treasure"')
        treasure_series = treasure_elements.loc[random.choice(treasure_elements.index), ]
        treasure = utilities.import_element(treasure_series)

        treasure.location = place_element(room, treasure.size)
        treasure.gold = gold_budget - current_gold
        elements.append(treasure)

    return elements

def populate_room(room: Room,
                  xp_budget: int = 0,
                  gold_budget: int = 0,
                  challenge: str = None,
                  tags: Tags = []) -> Room:
    """Adds content to a room. The challenge of the room determines its safety
        and relative xp_budget, then elements are selected that match the tags
        to approximately match the budget of experience and gold.

    Args:
        room: The Room to work on.
        xp_budget: The budget of experience to allocate between the
            elements in the room.
        gold_budget: The budget for gold value to allocate between the items in
            the room.
        shape: The vertices of the room.
        challenge: The relative difficulty of the room.
        tags: The thematic attributes of the room to sync elements to.

    Returns:
        A Room with completed attributes.
    """

    if challenge is None:
        challenge = random.choice(valid_challenges)
    room.challenge = challenge
    xp_budget *= challenge_multipliers[challenge]

    challenge_safety_mapping = {'Trivial': 'Safe',
                                'Easy': 'Sheltered',
                                'Medium': 'Risky',
                                'Hard': 'Unsafe',
                                'Deadly': 'Unsafe'}

    room.safety = challenge_safety_mapping[challenge]

    if tags == []:
        tags = [random.choice(universal_tags)]
    room.tags = room.tags + tags

    viable_tags = room.tags + ['neutral']
    viable_rooms = room_df[[utilities.filter_by_tags(r, viable_tags) for r in room_df.tags]]

    r_series = viable_rooms.loc[random.choice(viable_rooms.index), ]

    # TODO: follow other room rules here
    room.flavour = r_series.flavour

    room.elements = select_elements(room, xp_budget, gold_budget)

    return room

# TODO: add more sophisticated layout algorithms
def generate_dungeon_structure(n_rooms: int,
                                layout: str = 'linear',
                                **kwargs) -> Dungeon:
    """Creates a barren, connected dungeon.

    Args:
        n_rooms: The number of rooms to be created.
        layout: The algorithm used to link rooms into a graph. Defaults to 'linear'.
            Supported options are: 'linear'.
        **kwargs: Additional named parameters to be passed to the layout algorithm.

    Returns:
        A barren dungeon with rooms that only have an ID and connections.
    """

    def shape_generation():
        length = random.randrange(2,10)
        width = random.randrange(2,10)

        shape = [(0,0), (length,0), (length,width), (0,width)]
        return shape

    rooms = [Room(id=i, shape=shape_generation()) for i in range(n_rooms)]

    if layout == 'linear':
        current_y_offset = 0
        current_x_offset = 0
        for i in range(n_rooms):

            rooms[i].coord = (current_x_offset, current_y_offset)

            if i < (n_rooms - 1):
                wall_a = max(l[0] for l in rooms[i].shape)
                wall_b = 0
                width_a = max(l[1] for l in rooms[i].shape) - 1
                width_b = max(l[1] for l in rooms[i+1].shape) - 1

                # FIXME: does not work for rooms of width 1
                connection_a_y = random.randrange(0, width_a)
                connection_b_y = random.randrange(0, width_b)

                connection_a = (i+1, '', (wall_a, connection_a_y))
                connection_b = (i, '', (wall_b, connection_b_y))

                rooms[i].connections = rooms[i].connections + [connection_a]
                rooms[i+1].connections = rooms[i+1].connections + [connection_b]

                current_x_offset += wall_a
                current_y_offset += connection_a_y - connection_b_y
    else:
        raise ValueError(f'Invalid layout {layout}')

    return rooms

def generate_dungeon(n_rooms: int,
    party_level: int = 1, party_size: int = 4,
    layout: str = 'linear', **kwargs) -> Dungeon:
    """Creates a dungeon from scratch. Scales to level and size of party.

    Args:
        n_rooms: The number of rooms to be created.
        layout: The algorithm used to link rooms into a graph. Defaults to 'linear'.
            Supported options are: 'linear'.
        **kwargs: Additional named parameters to be passed to the layout algorithm.

    Returns:
        A Dungeon composed of Rooms with completed attributes.
    """

    base_xp_budget = xp_scaling[str(party_level)]
    # TODO: implement more sophisticated approach
    # http://redkatart.com/dnd5tools/
    # http://donjon.bin.sh/5e/random/#type=treasure
    total_gold_budget = 500*party_level
    gold_budget_per_room = round(total_gold_budget / n_rooms)

    dungeon = generate_dungeon_structure(n_rooms, layout, **kwargs)

    # Generates connection types
    # If not yet set, checks opposite side of connection and matches
    # If that is also not yet set, generates randomly
    for r in dungeon:
        for c in r.connections:
            if c[2] == '':
                matching_connection = d[c[1]][2]
                if matching_connection == '':
                    connection_type = random.choice(room_connection_types)
                    c[2], d[c[1]][2] = connection_type

    populated_dungeon = [populate_room(r,
        xp_budget=base_xp_budget,
        gold_budget=gold_budget_per_room)
        for r in dungeon]

    return populated_dungeon
