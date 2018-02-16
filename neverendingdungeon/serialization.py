# TODO: add json dungeon saving

from classes import *
import generation
import svgwrite
from typing import List


# TODO: add grid lines
def generate_svg_map(dungeon: List[Room], dungeon_name: str ="dev"):
    dmap = svgwrite.Drawing(filename=f"../output/{dungeon_name}_dungeonmap.svg", size=(10cm, 10cm))

    def draw_room(room: Room):
        room_svg = svgwrite.container.Group()
        abs_shape = [p + room.coord for p in room.shape]

        for c in room.connections:
            c_start = c[2] + room.coord
            c_end = (c_start[0], c_start[1] + 1)
            c_svg = svgwrite.shapes.Line(start=c_start, end=c_end)
            room_svg.add(c_svg)

        for e in room.elements:
            e_pos = e.location + room.coord
            e_svg = svgwrite.shapes.Circle(center=(e_pos[0] + 0.5, e_pos[1] + 0.5))
            room_svg.add(e_svg)

        walls_svg = svgwrite.shapes.Polygon(abs_shape)
        room_svg.add(walls_svg)
        return room_svg

    for r in dungeon:
        dmap.add(draw_room(r))

    dmap.save()

    return dmap
