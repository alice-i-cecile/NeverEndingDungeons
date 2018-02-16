# TODO: add json dungeon saving

from classes import *
import generation
import svgwrite
from typing import List


# TODO: add grid lines
def generate_svg_map(dungeon: List[Room], dungeon_name: str ="dev"):
    dmap = svgwrite.Drawing()

    # TODO: add connections
    # TODO: add element locations
    def draw_room(room: Room):
        room_svg = svgwrite.container.Group()
        abs_shape = room.shape + room.coord

        walls_svg = svgwrite.Polygon(abs_shape)
        return walls_svg

    for r in dungeon:
        dmap.add(draw_room(r))

    dmap.saveas(f"../output/{dungeon_name}_dungeonmap.svg")

    return dmap
