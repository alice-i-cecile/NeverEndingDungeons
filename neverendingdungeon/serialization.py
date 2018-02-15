# TODO: add json dungeon saving

from classes import *
import generation
import svgwrite


# TODO: add grid lines
def generate_svg_map(dungeon: generation.Dungeon):
    dmap = svgwrite.Drawing()

    # TODO: add connections
    # TODO: add element locations
    def draw_room(room: Room):
        room_svg = svgwrite.container.Group()
        abs_shape = room.shape + room.coord

        walls_svg = svgwrite.Polygon(abs_shape)
        return walls_svg

    for r in Dungeon:
        dmap.add(draw_room(r))

    dmap.saveas("../output/dev_dungeonmap.svg")

    return dmap
