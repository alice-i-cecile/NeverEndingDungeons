from classes import *
from content import *

from typing import Dict, Tuple, List, NewType
import random

Dungeon = List[Room]

# TODO: change to select_elements
def generate_element(element_type: str = None,
                     description: str = None,
                     gm_notes: str = None,
                     location: Location = None,
                     size: str = None,
                     tags: Tags = [],
                     **kwargs) -> Element:
    """Creates a random element to place in a room.

    Args:
        room: The Room to work on.
        description:

    Returns:
        An Element object with completed attributes.
    """


    if element_type is None:
        element_type <- random.choice(valid_element_types)

    element = {
        'Element': Element()
        'Interactable': Interactable()
        'NPC': NPC()
        'AbilityCheck': AbilityCheck()
    }[element_type]()

    if description is None:
        element.description = random.choice(element_descriptions)
    element.description = description

    if gm_notes is None:
        element.gm_notes = random.choice(element_gm_notess)
    element.gm_notes = gm_notes

    # TODO: generate within room bounds
    if location is None:
        element.location = (random.choice([0,1]), random.choice([0,1]))
    element.location = location

    if size is None:
        element.size = random.choice(element_sizes)
    element.size = size

    if tags is None:
        element.tags = random.choice(universal_tags)
    element.tags = tags

    # TODO: add support for using sane lookup system
    if element_type == 'Interactable':
        element = populate_interactable(element)

    if element_type == 'NPC':
        element = populate_npc(element)

    if element_type == 'AbilityCheck':
        element = populate_AbilityCheck(element)

    return element

def populate_room(room: Room,
                  xp_budget: int = 0,
                  gold_budget: int = 0,
                  shape: List[Position] = None,
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

    if shape is None:
        shape = [(0,0), (4,0), (4,4), (0,4)]
    room.shape = shape

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

    # TODO: add tag, xp, constraints
    # TODO: use select_elements approach
    for i in range(n_elements):

        selected_element = random.choice(elements_df.shape[0])
        e_series = element_df.iloc[selected_element, ]

        # TODO: is there a way to automatically apply matching names?
        # TODO: move into seperate import_element function in utilities.py
        if e_series.element_type == 'Base':
            new_element = Element(name = e_series.name,
                                  description = e_series.description,
                                  gm_notes = e_series.gm_notes,
                                  cr = e_series.cr,
                                  size = e_series.size,
                                  tags = e_series.tags)
        else if e_series.element_type == 'Interactable':
            new_element = Element(name = e_series.name,
                                  description = e_series.description,
                                  gm_notes = e_series.gm_notes,
                                  cr = e_series.cr,
                                  size = e_series.size,
                                  tags = e_series.tags,
                                  interaction_result = e_series.interaction_result)
        #TODO: add conversion of inventory to list
        else if e_series.element_type == 'NPC':
            new_element = Element(name = e_series.name,
                                  description = e_series.description,
                                  gm_notes = e_series.gm_notes,
                                  cr = e_series.cr,
                                  size = e_series.size,
                                  tags = e_series.tags,
                                  race = e_series.race,
                                  disposition = e_series.disposition,
                                  inventory = e_series.inventory
                                  )
        else if e_series.element_type == 'SkillCheck':
            new_element = Element(name = e_series.name,
                                  description = e_series.description,
                                  gm_notes = e_series.gm_notes,
                                  cr = e_series.cr,
                                  size = e_series.size,
                                  tags = e_series.tags,
                                  ability = e_series.ability,
                                  proficiency = e_series.proficency,
                                  difficulty = e_series.difficulty,
                                  success = e_series.success,
                                  failure = e_series.failure)
        else:
            raise ValueError(f"Invalid element_type {e_series.element_type}")

        # TODO: generate within room bounds
        element.location = (random.choice([0,1]), random.choice([0,1]))
        room.elements.append(new_element)

    return room

# TODO: set connection locations at this level
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

    rooms = [Room(id=i) for i in range(n_rooms)]

    if layout == 'linear':
        for i in range(n_rooms - 1):
            rooms[i].connections.append((RoomID(i+1), '', (0,0)))
            rooms[i+1].connections.append((RoomID(i), '', (0,0)))

    return rooms

#TODO: set connection types at this level
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
    populated_dungeon = map(populate_room, dungeon,
        xp_budget=base_xp_budget, gold_budget=gold_budget_per_room)

    return populated_dungeon
