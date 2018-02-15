# Contains standard use scenarios
# Intended to be run and inspected manually for debugging or demonstration

# FIXME: figure out how to run from tests directory instead
import generation
import serialization

my_tiny_dungeon = generation.generate_dungeon(n_rooms=1)
print(my_tiny_dungeon)
serialization.generate_svg_map(my_tiny_dungeon, 'tiny')

my_linear_dungeon = generation.generate_dungeon(n_rooms=5, layout='linear')
print(my_linear_dungeon)
serialization.generate_svg_map(my_tiny_dungeon, 'linear')
