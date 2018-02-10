from typing import Dict, Tuple, List, NewType

# TODO: describe this data type
DungeonGraph = NewType("DungeonGraph", any)

Dungeon = List[Room]

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
            rooms[i].connections.add((RoomID(i+1), "", (0,0)))
            rooms[i+1].connections.add((RoomID(i), "", (0,0)))

    return rooms

def populate_room(room: Room) -> Room:
    """Adds content to a room.

    Args:
        room: The Room to work on.

    Returns:
        A Room with completed attributes.
    """

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
