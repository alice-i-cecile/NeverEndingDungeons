from classes import *
from content import *
import utilities

from typing import Dict, Tuple, List, NewType
import random

Dungeon = List[Room]

# TODO: generalize for nonrectangular Rooms
# TODO: take size into account
def place_element(room: Room, size: str = "Medium"):
    x_coord = [l[0]] for l in r.shape]
    y_coord = [l[1]] for l in r.shape]

    # Items are placed at the centers of squares but walls are on edges
    x_min, y_min = min(x_coord), min(y_coord)
    x_max, y_max = max(x_coord) - 1, max(y_coord) - 1

    x, y = random.randrange(x_min, x_max), random.randrange(y_min, y_max)
    return (x,y)

def select_elements(room, xp_budget: int, gold_budget: int):

    tags = room.tags
    viable_tags = tags.append('neutral')

    def filter_by_tags(tags):
        tags = tags.split(sep=', ')
        return any(i in tags for i in valid_tags)

    viable_elements = element_df[filter_by_tags(element_df.tags)]

    # TODO: switch to a nonconvex optimization approach
    current_xp = 0
    while current_xp < xp_budget & len(room.elements) < 5:

        viable_elements = viable_elements.query('xp < xp_budget - current_xp')

        selected_element = random.choice(viable_elements.shape[0])
        e_series = element_df.iloc[selected_element, ]

        new_element = utilities.import_element(e_series)

        new_element.location = place_element(room.shape, new_element.size)
        room.elements.append(new_element)

        current_xp += new_element.xp

    current_gold = sum(e.gold for e in elements)
    if current_gold < gold_budget:
        # TODO: implement treasure element type
        treasure_elements = element_df.query('tag == "treaure"')

        selected_treasure = random.choice(viable_elements.shape[0])
        treasure_series = element_df.iloc[selected_element, ]

        treasure = utilities.import_element(e_series)

        # TODO: generate within room bounds
        treasure.location = place_element(room.shape, treasure.size)
        treasure.gold = gold_budget - current_gold
        room.elements.append(treasure)

    return room


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

    for i in range(room.connections):
        if connection_type is None:
            room.connections[i][2] = random.choice(room_connection_types)
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

    if challenge is None:
        challenge = random.choice(valid_challenges)
    room.challenge = challenge
    room.xp_budget *= challenge_multipliers[challenge]

    challenge_safety_mapping = {'Trivial': 'Safe',
                                'Easy': 'Sheltered',
                                'Medium': 'Risky',
                                'Hard': 'Unsafe',
                                'Deadly': 'Unsafe'}

    room.safety = challenge_safety_mapping[challenge]

    if tags is []:
        tags = random.choice(universal_tags)
    room.tags.append(tags)

    # TODO: change to penalized optimization approach
    n_elements = random.randrange(1,5)

    room.elements = select_elements(room, xp_budget, gold_budget, tags)

    return room

def generate_dungeon_structure(n_rooms: int,
                                layout: string = 'linear',
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
        length = random.randrange(1,10)
        width = random.randrange(1,10)

        shape = [(0,0), (length,0), (length,width), (0,width)]
        return shape

    rooms = [Room(id=i, shape=shape_generation()) for i in range(n_rooms)]

    if layout == 'linear':
        current_y_offset = 0
        current_x_offset = 0
        for i in range(n_rooms):

            rooms[i].coord = (current_x_offset, current_y_offset)

            length = max(l[1][0] for l in rooms[i].shape)

            if (i != n_rooms):
                wall_a = max(l[1][0] for l in rooms[i].shape)
                wall_b = 0
                width_a = max(l[1][1] for l in rooms[i].shape) - 1
                width_b = max(l[1][1] for l in rooms[i+1].shape) - 1
                connection_a_y = random.randrange(0, width_a)
                connection_b_y = random.randrange(0, width_b)

                rooms[i].connections.append(i+1, '',
                    (wall_a, connection_a_y))
                rooms[i+1].connections.append(i, '',
                    (wall_b, connection_b_y))

            current_x_offset += length
            current_y_offset += connection_a_y - connection_b_y
    else:
        raise ValueError(f'Invalid layout {layout}')

    return rooms

def generate_dungeon(n_rooms: int,
    party_level: int = 1, party_size: int = 4,
    layout='linear': string, **kwargs) -> Dungeon:
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
