# Contains standard use scenarios
# Intended to be run and inspected manually for debugging or demonstration

# FIXME: figure out how to run from tests directory instead
import generation
import serialization

my_tiny_dungeon = generation.generate_dungeon(n_rooms=1)
for room in my_tiny_dungeon:
    print(room)
serialization.generate_svg_map(my_tiny_dungeon, 'tiny')

my_linear_dungeon = generation.generate_dungeon(n_rooms=5, layout='linear')
for room in my_linear_dungeon:
    print(room)
serialization.generate_svg_map(my_tiny_dungeon, 'linear')
