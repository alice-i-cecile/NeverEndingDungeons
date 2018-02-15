# Contains standard use scenarios
# Intended to be run and inspected manually for debugging or demonstration

from context import neverendingdungeon as ned

my_tiny_dungeon = ned.generation.generate_dungeon(n_rooms=1)
print(my_tiny_dungeon)
ned.serialization.generate_svg_map(my_tiny_dungeon, 'tiny')

my_linear_dungeon = ned.generation.generate_dungeon(n_rooms=5, layout='linear')
print(my_linear_dungeon)
ned.serialization.generate_svg_map(my_tiny_dungeon, 'linear')
