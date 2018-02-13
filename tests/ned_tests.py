from context import neverendingdungeon

from hypothesis import given, example
from hypothesis.strategies import integers, sampled_from, random_module
import random

# Element-level tests ####
@given(sampled_from('Element', 'Interactable', 'NPC', 'SkillCheck'), random_module())
def test_element_field_validity(element_type):
    element = neverendingdungeon.generation.generate_element(element_type)

    valid_sizes = ['Tiny', 'Small', 'Medium', 'Large', 'Huge', 'Gargantuan']
    assert element.size in valid_sizes

    if type(element) == Interactable:
        pass
    else if type(element) == NPC:
        valid_dispositions = ['Hostile', 'Unfriendly', 'Indifferent', 'Friendly', 'Helpful']
        assert (element.disposition in valid_dispositions), \
            f'Invalid disposition {element.disposition}'
    else if type(element) == SkillCheck:
        valid_abilities = ['Strength', 'Constitution',
                           'Dexterity', 'Intelligence',
                           'Wisdom', 'Charisma']
        assert all((i for i in element.ability) in valid_abilities),\
            f'Invalid ability {element.ability}'
        valid_skills = ['None',
                        'Athletics',
                        'Acrobatics', 'Sleight of Hand', 'Stealth',
                        'Arcana', 'History', 'Investigation', 'Nature', 'Religion',
                        'Animal Handling', 'Insight', 'Medicine', 'Perception', 'Survival',
                        'Deception', 'Intimidation', 'Performance', 'Persuasion']
        assert all((i for i in element.skill) in valid_skills),
            f'Invalid ability {element.skill}'

@given(sampled_from('Element', 'Interactable', 'NPC', 'SkillCheck'), random_module())
def test_unchanged_element_defaults(element_type):
    element = neverendingdungeon.generation.generate_element(element_type)

    assert element.description != '', 'Empty description attribute'
    assert element.gm_notes != '', 'Empty gm_notes attribute'
    assert element.location != Position((-1,-1)), 'Unchanged location attribute'
    assert element.size != Size(''), 'Empty size attribute'
    assert element.tags != [], 'Empty tags attribute'

    if type(element) == Interactable:
        assert element.interaction_result != '', 'Empty interaction_result attribute'
    else if type(element) == NPC:
        assert element.race != '', 'Empty race attribute'
        assert element.disposition != '', 'Empty disposition attribute'
        # Empty inventory is valid
    else if type(element) == SkillCheck:
        assert element.ability != [], 'Empty ability attribute'
        assert element.skill != [], 'Empty skill attribute'
        assert element.success != '', 'Empty success attribute'
        assert element.failure != '', 'Empty failure attribute'

# Room level tests ####
@given(random_module())
def test_elements_in_room():
    empty_room = neverendingdungeon.classes.Room(id=1)
    room = neverendingdungeon.generation.populate_room(empty_room)

    # TODO: implement for nonrectangular rooms
    def is_in_room(location, polygon):
        x_coord = [l[0]] for l in r.shape]
        y_coord = [l[1]] for l in r.shape]

        valid_x = location[0] > min(x_coord) & location[1] < max(x_coord)
        valid_y = location[0] > min(y_coord) & location[1] < max(y_coord)

        return valid_x & valid_y

    for e in room.elements:
        assert is_in_room(e.location, room.shape), \
            f'element {e} at {e.location} is not in room'

@given(random_module())
def test_room_field_validity():
    empty_room = neverendingdungeon.classes.Room(id=1)
    room = neverendingdungeon.generation.populate_room(empty_room)

    valid_challenges = ['Trivial', 'Easy', 'Medium', 'Hard', 'Deadly']
    assert room.challenge in valid_challenges, \
        f'Invalid challenge {room.challenge}'

    valid_safetys = ['Unsafe', 'Risky', 'Sheltered', 'Safe']
    assert room.safety in valid_safetys, \
        f'Invalid safety {room.safty}'

@given(random_module())
def test_unchanged_room_defaults():
    empty_room = neverendingdungeon.classes.Room(id=1)
    room = neverendingdungeon.generation.populate_room(empty_room)

    assert room.shape != [], 'Empty shape attribute'
    # Connections are tested at the dungeon level
    assert room.elements != [], 'Empty elements attribute'
    assert room.challenge != Challenge(''), 'Empty challenge attribute'
    assert room.safety != Safety(''), 'Empty safety attribute'
    assert room.flavour != '', 'Empty flavour attribute'
    assert room.tags != [], 'Empty tags attribute'

@given(integers(min_value=1, max_value=4), random_module())
def test_connections_on_wall(n_connections):
    empty_room = neverendingdungeon.classes.Room(id=1)
    for i in range(n_connections):
        empty_room.connections.append((RoomID(2+i), "", (0,0)))

    room = neverendingdungeon.generation.populate_room(empty_room)

    for connection in room_a.connections:
        # TODO: generalize to nonrectangular rooms
        x_coord = [l[0]] for l in room.shape]
        y_coord = [l[1]] for l in room.shape]

        h = connection[3][0] in [min(x_coord), max(x_coord)]
        v = connection[3][1] in [min(y_coord), max(y_coord)]

        assert (h or v), 'Connection is not on wall'

# Dungeon level tests ####
@given(integers(min_value=1), random_module())
def test_unique_roomID(n_rooms):
    dungeon = neverendingdungeon.generation.generate_dungeon(n_rooms)

    roomIDs = [r.id for r in dungeon]
    assert len(set(roomIds)) == len(roomIDs), 'RoomIDs are not unique'

@given(integers(min_value=1), random_module())
def test_uniqueness_connections(n_rooms):
    dungeon = neverendingdungeon.generation.generate_dungeon(n_rooms)

    for room in dungeon:
        for connection in room.connections:
            connections_id = [c[1] for c in room.connections]
            assert  len(set(connections_id)) == len(connections_id), \
                f'Duplicate connection from room {room.id}'

@given(integers(min_value=1), random_module())
def test_bidirectional_connections(n_rooms):
    dungeon = neverendingdungeon.generation.generate_dungeon(n_rooms)

    for room_a in dungeon:
        for connection_a in room_a.connections:
            room_b = dungeon[connection_a[0]]
            connections_b = [c[0] for c in room_b.connections]
            assert room_a.id in connections_b, \
                f'Connection between {room_a.id} \
                and {room_b.id} is not biderectional'

@given(integers(min_value=1), random_module())
def test_connection_side_matching(n_rooms):
    dungeon = neverendingdungeon.generation.generate_dungeon(n_rooms)

    for room_a in dungeon:
        for connection_a in room_a.connections:
            room_b = dungeon[connection[0]]
            connection_b = filter(c[0] == room_a.id for c in room_b.connections)

            # TODO: generalize to nonrectangular rooms
            def get_facing(c, r):
                x_coord = [l[0]] for l in r.shape]
                y_coord = [l[1]] for l in r.shape]

                if c[3][0] == min(x_coord):
                    return 'left'
                else if c[3][0] == max(x_coord):
                    return 'right'
                else if c[3][1] == min(y_coord):
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

            assert complementary(facing_a, facing_b),
                f'Connection between {room_a.id} and {room_b.id} is misaligned'
