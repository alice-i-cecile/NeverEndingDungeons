from context import neverendingdungeon

from hypothesis import given, example
from hypothesis.strategies import integers, sampled_from, random_module
import random

# Element-level tests ####
@given(sampled_from('Element', 'Interactable', 'NPC', 'SkillCheck'), random_module())
def test_element_field_validity(element_type):
    element = neverending_dungeon.generation.generate_element(element_type)

    valid_sizes = ['Tiny', 'Small', 'Medium', 'Large', 'Huge', 'Gargantuan']
    assert element.size in valid_sizes

    if type(element) == Interactable:
        pass
    else if type(element) == NPC:
        valid_dispositions = ['Hostile', 'Unfriendly', 'Indifferent', 'Friendly', 'Helpful']
        assert (element.disposition in valid_dispositions)
    else if type(element) == SkillCheck:
        valid_abilities = ['Strength', 'Constitution', 'Dexterity', 'Intelligence', 'Wisdom', 'Charisma']
        assert all((i for i in element.ability) in valid_abilities)

        valid_skills = ['None',
                        'Athletics',
                        'Acrobatics', 'Sleight of Hand', 'Stealth',
                        'Arcana', 'History', 'Investigation', 'Nature', 'Religion',
                        'Animal Handling', 'Insight', 'Medicine', 'Perception', 'Survival',
                        'Deception', 'Intimidation', 'Performance', 'Persuasion']
        assert all((i for i in element.ability) in valid_abilities)


@given(sampled_from('Element', 'Interactable', 'NPC', 'SkillCheck'), random_module())
def test_unchanged_element_defaults(element_type):
    element = neverending_dungeon.generation.generate_element(element_type)

    assert element.description != ''
    assert element.gm_notes != ''
    assert element.location != Position((-1,-1))
    assert element.size != Size('')
    assert element.tags != []

    if type(element) == Interactable:
        assert element.interaction_result != ''
    else if type(element) == NPC:
        assert element.race != ''
        assert element.disposition != ''
        # Empty inventory is valid
    else if type(element) == SkillCheck:
        assert element.ability != []
        assert element.skill != []
        assert element.success != ''
        assert element.failure != ''

# Room level tests ####
@given(random_module())
def test_elements_in_room():
    room = neverending_dungeon.generation.populate_room(Room(id=1))

    # TODO: implement polygon checking
    def is_in_room(location, polygon):
        return True

    for e in room.elements:
        assert is_in_room(e.location, room.shape)

@given(random_module())
def test_room_field_validity():
    room = neverending_dungeon.generation.populate_room(Room(id=1))

    valid_challenges = ['Trivial', 'Easy', 'Medium', 'Hard', 'Deadly']
    assert room.challenge in valid_challenges

    valid_safetys = ['Unsafe', 'Risky', 'Sheltered', 'Safe']
    assert room.safety in valid_safetys

@given(random_module())
def test_unchanged_room_defaults():
    room = neverending_dungeon.generation.populate_room(Room(id=1))

    assert room.shape != []
    # Connections are tested at the dungeon level
    assert room.elements != []
    assert room.challenge != Challenge('')
    assert room.safety != Safety('')
    assert room.flavour != ''
    assert room.tags != []

# Dungeon level tests ####
@given(integers(min_value=1), random_module())
def test_unique_roomID(n_rooms):
    dungeon = neverending_dungeon.generation.generate_dungeon(n_rooms)

    roomIDs = [r.id for r in dungeon]
    assert len(set(roomIds)) == len(roomIDs)

@given(integers(min_value=1), random_module())
def test_uniqueness_connections(n_rooms):
    dungeon = neverending_dungeon.generation.generate_dungeon(n_rooms)

    for room in dungeon:
        for connection in room_a.connections:
            connections_id = [c[1] for c in room.connections]
            assert  len(set(connections_id)) == len(connections_id)

#TODO: refactor so can be moved to room level tests
@given(integers(min_value=1), random_module())
def test_connections_on_wall(n_rooms):
    dungeon = neverending_dungeon.generation.generate_dungeon(n_rooms)

    for room in dungeon:
        for connection in room_a.connections:

            # TODO: generalize to nonrectangular rooms
            x_coordinates = [l[0]] for l in room.shape]
            y_coordinates = [l[1]] for l in room.shape]

            h = connection[3][0] in [min(x_coordinates), max(x_coordinates)]
            v = connection[3][1] in [min(y_coordinates), max(y_coordinates)]

            assert (h or v)

@given(integers(min_value=1), random_module())
def test_bidirectional_connections(n_rooms):
    dungeon = neverending_dungeon.generation.generate_dungeon(n_rooms)

    for room_a in dungeon:
        for connection_a in room_a.connections:
            room_b = dungeon[connection_a[0]]
            connections_b = [c[0] for c in room_b.connections]
            assert room_a.id in connections_b

@given(integers(min_value=1), random_module())
def test_connection_side_matching(n_rooms):
    dungeon = neverending_dungeon.generation.generate_dungeon(n_rooms)

    for room_a in dungeon:
        for connection_a in room_a.connections:
            room_b = dungeon[connection[0]]
            connection_b = filter(c[0] == room_a.id for c in room_b.connections)

            # TODO: generalize to nonrectangular rooms
            def get_facing(c, r):
                x_coordinates = [l[0]] for l in r.shape]
                y_coordinates = [l[1]] for l in r.shape]

                if c[3][0] == min(x_coordinates):
                    return 'left'
                else if c[3][0] == max(x_coordinates):
                    return 'right'
                else if c[3][1] == min(y_coordinates):
                    return 'bottom'
                else:
                    return 'top'

            def complementary(f_a, f_b):
                if f_a == 'left' and f_b == 'right':
                    return True
                else if f_a == 'right' and f_b == 'left':
                    return True
                else if f_a == 'top' and f_b == 'bottom':
                    return True
                else if f_a == 'bottom' and f_b == 'top':
                    return True
                else:
                    return False

            facing_a = get_facing(connection_a, room_a)
            facing_b = get_facing(connection_b, room_b)

            assert complementary(facing_a, facing_b)
