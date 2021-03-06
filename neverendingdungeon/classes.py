# TODO: add __print__ magic methods to Element and Room

from typing import Dict, Tuple, List, NewType

# FIXME: "To annotate arguments it is preferred to use abstract
# collection types such as Mapping, Sequence, or AbstractSet."

# Cartesian grid, with origin in bottom-left corner
Position = Tuple[int, int]
Tags = List[str]

# RoomID, ConnectionType, ConnectionLocation
Connection = Tuple[int, str, Position]

# TODO: add docstrings
# TODO: make gold derived property
class Element:
    def __init__(self,
                name: str = '',
                description: str = '',
                gm_notes: str = '',
                cr: str = 0,
                xp: int = 0,
                gold: int =0,
                location: Position  = (-1, -1),
                size: str = '',
                tags: Tags = []):
        self.description = description
        self.gm_notes = gm_notes
        self.cr = cr
        self.xp = xp
        self.gold = gold
        self.location = location
        self.size = size
        self.tags = tags

    def __str__(self):
        pretty_str = str(vars(self))
        return pretty_str

class Interactable(Element):
    def __init__(self,
                name: str = '',
                description: str = '',
                gm_notes: str = '',
                cr: str = 0,
                xp: int = 0,
                gold: int =0,
                location: Position  = (-1, -1),
                size: str = '',
                tags: Tags = [],
                interaction_result: str = ''):
        super().__init__(name, description, gm_notes, cr, xp, gold, location, size, tags)
        self.interaction_result = interaction_result


# FIXME: descriptions may want to be handled per group of NPCs,
# rather than on an individual level
class NPC(Element):
    def __init__(self,
                name: str = '',
                description: str = '',
                gm_notes: str = '',
                cr: str = 0,
                xp: int = 0,
                gold: int = 0,
                location: Position  = (-1, -1),
                size: str = '',
                tags: Tags = [],
                race: str = '',
                disposition: str = '',
                inventory: List[str] = []):
        super().__init__(name, description, gm_notes, cr, xp, gold, location, size, tags)
        self.race = race
        self.disposition = disposition
        self.inventory = inventory

class AbilityCheck(Element):
    def __init__(self,
                name: str = '',
                description: str = '',
                gm_notes: str = '',
                cr: str = 0,
                xp: int = 0,
                gold: int =0,
                location: Position  = (-1, -1),
                size: str = '',
                tags: Tags = [],
                ability: str = '',
                proficiency: str = '',
                difficulty: int = '',
                success: str = '',
                failure: str = ''):

        super().__init__(name, description, gm_notes, cr, xp, gold, location, size, tags)

        self.ability = ability
        self.proficiency = proficiency
        self.difficulty = difficulty
        self.success = success
        self.failure = failure

class Treasure(Element):
    def __init__(self,
                name: str = '',
                description: str = '',
                gm_notes: str = '',
                cr: str = 0,
                xp: int = 0,
                gold: int =0,
                location: Position  = (-1, -1),
                size: str = '',
                tags: Tags = [],
                contents: List[str] = []):

        super().__init__(name, description, gm_notes, cr, xp, gold, location, size, tags)

        self.contents = contents

class Room:
    def __init__(self,
                id: int,
                coord: Position = (0,0),
                shape: List[Position] = [],
                connections: List[Connection] = [],
                elements: List[Element] = [],
                challenge: str = '',
                safety: str = '',
                flavour: str = '',
                tags: Tags = []):
        # RoomID corresponds to the room position in the Dungeon list
        self.id = id
        self.shape = shape
        self.connections = connections
        self.elements = elements
        self.flavour = flavour
        self.challenge = challenge
        self.safety = safety
        self.tags = tags

    def __str__(self):
        pretty_str = str(vars(self))
        return pretty_str
