from context import neverendingdungeon as ned

from hypothesis import given, example
from hypothesis.strategies import integers, sampled_from, random_module, lists, tuples
import random

# Element-level tests ####
@given(sampled_from(['Element', 'Interactable', 'NPC', 'SkillCheck']),
       sampled_from(ned.content.valid_sizes),
       sampled_from(ned.content.valid_dispositions),
       sampled_from(ned.content.valid_abilities),
       sampled_from(ned.content.valid_skills))
def test_element_field_validity(element_type,
                                size,
                                disposition,
                                ability,
                                skill):
    element = ned.generation.generate_element(element_type=element_type,
                                size=size,
                                disposition=disposition,
                                ability=ability,
                                skill=skill)

    assert element.size in ned.content.valid_sizes, \
        f{'Invalid size {element.size}'}

    if element_type == 'Interactable':
        pass
    else if element_type == 'NPC':
        assert (element.disposition in ned.content.valid_dispositions), \
            f'Invalid disposition {element.disposition}'
    else if element_type == 'SkillCheck':

        assert all((i for i in element.ability) in ned.content.valid_abilities), \
            f'Invalid ability {element.ability}'

        assert all((i for i in element.skill) in ned.content.valid_skills), \
            f'Invalid ability {element.skill}'

@given(sampled_from('Element', 'Interactable', 'NPC', 'SkillCheck'),
       sampled_from(ned.content.element_descriptions),
       sampled_from(ned.content.element_gm_notes),
       tuples(integers(0,1),integers(0,1)),
       sampled_from(ned.content.valid_sizes),
       lists(sampled_from(ned.content.universal_tags)
       sampled_from(ned.content.interaction_results),
       sampled_from(ned.content.npc_races),
       sampled_from(ned.content.valid_dispositions),
       lists(sampled_from(ned.content.valid_abilities)),
       lists(sampled_from(ned.content.valid_skills)),
       lists(integers(0,40)),
       sampled_from(ned.content.check_successes),
       sampled_from(ned.content.check_failures))
def test_unchanged_element_defaults(element_type,
                                    description,
                                    gm_notes,
                                    location,
                                    size,
                                    tags,
                                    interaction_result,
                                    race,
                                    disposition,
                                    ability,
                                    skill,
                                    difficulty,
                                    success,
                                    failure):
    element = ned.generation.generate_element(element_type,
        description = description,
        gm_notes = gm_notes,
        location = location,
        size = size,
        tags = tags,
        interaction_result = interaction_result,
        race = race,
        disposition = disposition,
        ability = ability,
        skill = skill,
        difficulty = difficulty,
        success = success,
        failure = failure)

    assert element.description != '', 'Empty description attribute'
    assert element.gm_notes != '', 'Empty gm_notes attribute'
    assert element.location != Position((-1,-1)), 'Unchanged location attribute'
    assert element.size != Size(''), 'Empty size attribute'
    assert element.tags != [], 'Empty tags attribute'

    if element_type == 'Interactable':
        assert element.interaction_result != '', 'Empty interaction_result attribute'
    else if element_type == 'NPC':
        assert element.race != '', 'Empty race attribute'
        assert element.disposition != '', 'Empty disposition attribute'
        # Empty inventory is valid
    else if element_type == 'SkillCheck':
        assert element.ability != [], 'Empty ability attribute'
        assert element.skill != [], 'Empty skill attribute'
        assert element.success != '', 'Empty success attribute'
        assert element.failure != '', 'Empty failure attribute'

# Room level tests ####
@given(integers(1, 10), random_module())
def test_elements_in_room(n_elements):
    empty_room = ned.classes.Room(id=1)
    room = ned.generation.populate_room(empty_room, n_elements=n_elements)

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

@given(sampled_from(ned.content.valid_challenges),
       sampled_from(ned.content.valid_safetys)
def test_room_field_validity(challenge, safety):
    empty_room = ned.classes.Room(id=1)
    room = ned.generation.populate_room(empty_room,
        challenge=challenge, safety=safety)

    assert room.challenge in ned.content.valid_challenges, \
        f'Invalid challenge {room.challenge}'

    assert room.safety in ned.content.valid_safetys, \
        f'Invalid safety {room.safty}'

@given(integers(1,10),
       lists(tuples(integers(0,10), integers(0,10)), min_size = 2, max_size = 10),
       sampled_from(ned.content.room_connection_types),
       sampled_from(['Trivial', 'Easy', 'Medium', 'Hard', 'Deadly']),
       sampled_from(['Unsafe', 'Risky', 'Sheltered', 'Safe']))
       sampled_from(ned.content.room_flavour)
def test_unchanged_room_defaults(n_elements,
                                 shape,
                                 connection_type,
                                 challenge,
                                 safety,
                                 flavour):
    empty_room = ned.classes.Room(id=1,
                                 n_elements = n_elements,
                                 shape = shape,
                                 connection_type = connection_type,
                                 challenge = challenge,
                                 safety = safety,
                                 flavour = flavour)
    room = ned.generation.populate_room(empty_room)

    assert room.shape != [], 'Empty shape attribute'
    # Connections are tested at the dungeon level
    assert room.elements != [], 'Empty elements attribute'
    assert room.challenge != Challenge(''), 'Empty challenge attribute'
    assert room.safety != Safety(''), 'Empty safety attribute'
    assert room.flavour != '', 'Empty flavour attribute'
    assert room.tags != [], 'Empty tags attribute'

@given(integers(min_value=1, max_value=4))
def test_connections_on_wall(n_connections):
    empty_room = ned.classes.Room(id=1)
    for i in range(n_connections):
        empty_room.connections.append((RoomID(2+i), '', (0,0)))

    room = ned.generation.populate_room(empty_room)

    for connection in room_a.connections:
        # TODO: generalize to nonrectangular rooms
        x_coord = [l[0]] for l in room.shape]
        y_coord = [l[1]] for l in room.shape]

        h = connection[3][0] in [min(x_coord), max(x_coord)]
        v = connection[3][1] in [min(y_coord), max(y_coord)]

        assert (h or v), 'Connection is not on wall'

# Dungeon level tests ####
@given(integers(min_value=1))
def test_unique_roomID(n_rooms):
    dungeon = ned.generation.generate_dungeon(n_rooms)

    roomIDs = [r.id for r in dungeon]
    assert len(set(roomIds)) == len(roomIDs), 'RoomIDs are not unique'

@given(integers(min_value=1))
def test_uniqueness_connections(n_rooms):
    dungeon = ned.generation.generate_dungeon(n_rooms)

    for room in dungeon:
        for connection in room.connections:
            connections_id = [c[1] for c in room.connections]
            assert  len(set(connections_id)) == len(connections_id), \
                f'Duplicate connection from room {room.id}'

@given(integers(min_value=1))
def test_bidirectional_connections(n_rooms):
    dungeon = ned.generation.generate_dungeon(n_rooms)

    for room_a in dungeon:
        for connection_a in room_a.connections:
            room_b = dungeon[connection_a[0]]
            connections_b = [c[0] for c in room_b.connections]
            assert room_a.id in connections_b, \
                f'Connection between {room_a.id} \
                and {room_b.id} is not biderectional'

@given(integers(min_value=1))
def test_connection_side_matching(n_rooms):
    dungeon = ned.generation.generate_dungeon(n_rooms)

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
