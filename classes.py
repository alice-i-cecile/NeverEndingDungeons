from typing import Dict, Tuple, List, NewType
# FIXME: "To annotate arguments it is preferred to use abstract
# collection types such as Mapping, Sequence, or AbstractSet."


ElementID = NewType('ElementID', int)
RoomID = NewType('RoomID', int)

Position = Tuple[int, int]
# oneof ("Tiny", "Small", "Medium", "Large", "Huge", "Gargantuan")
Size =  NewType("Size", str)
Tags = List[str]

# oneof (“Hostile”, “Unfriendly”, “Indifferent”, “Friendly”, “Helpful”)
Disposition = NewType("Disposition", str)
# oneof ("Strength", "Dexterity", "Constitution",
# "Intelligence", "Wisdom", "Charisma")
Ability = NewType("Ability", str)
# one of the 5e skills or "None"
Skill = NewType("Skill", str)


ConnectionType = NewType('ConnectionType', str)
Connection = Tuple[Room, ConnectionType, Position]
# oneof  (“Trivial”, “Easy”, “Medium”, “Difficult”, “Deadly”)
Challenge = NewType('Challenge', str)
# oneof (“Unsafe”, “Risky”, “Sheltered”, “Safe”)
Safety = NewType('Safety', str)

class Element:
    def __init__(self, id: ElementID,
                description: str, gm_notes: str,
                location: Position,
                size: Size,
                tags: Tags):
        self.id = id
        self.description = description
        self.gm_notes = gm_notes
        self.location = location
        self.size = size
        self.tags = tags

class Interactable(Element):
    def __init__(self, id: ElementID,
                description: str, gm_notes: str,
                location: Position,
                tags: Tags,
                interaction_result: str):
        super().__init__(self, id, description, gm_notes, location, size, tags)
        self.interaction_result = interaction_result


# FIXME: descriptions may want to be handled per group of NPCs,
# rather than on an individual level
class NPC(Element):
    def __init__(self, id: ElementID,
                description: str, gm_notes: str,
                location: Position,
                tags: Tags,
                interaction_result: str,
                race: str,
                disposition: Disposition
                inventory: List(string)):
        super().__init__(self, id, description, gm_notes, location, size, tags)
        self.race = race
        self.disposition = disposition
        self.inventory = inventory

class SkillCheck(Element):
    def __init__(self, id: ElementID,
                description: str, gm_notes: str,
                location: Position,
                tags: Tags,
                interaction_result: str,
                ability: List[Ability],
                skill: List[Skill],
                difficulty: List[int],
                success: str,
                failure: str):

        super().__init__(self, id, description, gm_notes, location, size, tags)

        self.ability = ability
        self.skill = skill
        self.difficulty = difficulty
        self.success = success
        self.failure = failure

class Room:
    def __init__(self, id: RoomID,
                shape: List[Position],
                connections: List[Connection],
                elements: List[Element],
                challenge: Challenge,
                safety: Safety,
                flavour: str,
                tags: Tags):
        self.id = id
        self.shape = shape
        self.connections = connections
        self.elements = elements
        self.flavour = flavour
        self.challenge = challenge
        self.safety = safety
        self.tags = tags
