from hypothesis import given, example
from hypothesis.strategies import integers, sampled_from
import random

# Element-level tests ####
@given(integers(), sampled_from('Element', 'Interactable', 'NPC', 'SkillCheck'))
def test_element_field_validity(seed, element_type):
    random.seed(seed)
    element = generate_element(element_type)

@given(integers(), sampled_from('Element', 'Interactable', 'NPC', 'SkillCheck'))
def test_unchanged_element_defaults(seed, element_type):
    random.seed(seed)
    element = generate_element(element_type)


# Room level tests ####
@given(integers())
def test_elements_in_room(seed):
    random.seed(seed)
    room = populate_room(Room(id=1))


# Dungeon level tests ####
@given(integers(), integers(min_value=1))
def test_unique_roomID(seed, n_rooms):
    random.seed(seed)
    dungeon = generate_dungeon(n_rooms)

@given(integers(), integers(min_value=1))
def test_room_field_validity(seed, n_rooms):
    random.seed(seed)
    dungeon = generate_dungeon(n_rooms)

@given(integers(), integers(min_value=1))
def test_unchanged_room_defaults(seed, n_rooms):
    random.seed(seed)
    dungeon = generate_dungeon(n_rooms)

@given(integers(), integers(min_value=1))
def test_bidirectional_connections(seed, n_rooms):
    random.seed(seed)
    dungeon = generate_dungeon(n_rooms)

@given(integers(), integers(min_value=1))
def test_connection_side_matching(seed, n_rooms):
    random.seed(seed)
    dungeon = generate_dungeon(n_rooms)
