"""Barrels prop implementation."""

import math
import skia
from typing import TYPE_CHECKING

from dungeongen.graphics.shapes import Circle, Rectangle
from dungeongen.graphics.aliases import Point
from dungeongen.constants import CELL_SIZE
from dungeongen.map._props.prop import Prop, PropType
from dungeongen.map.enums import Layers
from dungeongen.graphics.rotation import Rotation

if TYPE_CHECKING:
    from dungeongen.map.map import Map

BARREL_RADIUS = CELL_SIZE * 0.25

BARRELS_PROP_TYPE = PropType(
    is_grid_aligned=True,
    boundary_shape=Circle(0, 0, BARREL_RADIUS),
    grid_size=(1, 1)
)

class Barrels(Prop):
    """Small cylindrical containers with staves and bands, drawn as a circle with vertical and horizontal lines."""

    def __init__(self, position: Point, rotation: Rotation = Rotation.ROT_0) -> None:
        super().__init__(BARRELS_PROP_TYPE, position, rotation=rotation)

    def _draw_content(self, canvas: skia.Canvas, bounds: Rectangle, layer: Layers = Layers.PROPS) -> None:
        if layer != Layers.PROPS:
            return

        options = self._map.options if self._map else None
        stroke = options.prop_stroke_width if options else 2.0
        fill_color = options.prop_fill_color if options else 0xFFFFFFFF
        outline_color = options.prop_outline_color if options else 0xFF000000

        fill = skia.Paint(AntiAlias=True, Style=skia.Paint.kFill_Style, Color=fill_color)
        canvas.drawCircle(0, 0, BARREL_RADIUS, fill)

        outline = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=stroke, Color=outline_color)
        canvas.drawCircle(0, 0, BARREL_RADIUS, outline)

        stave_count = 6
        for i in range(stave_count):
            angle = i * (360.0 / stave_count)
            rad = math.radians(angle)
            x1 = math.cos(rad) * BARREL_RADIUS * 0.3
            y1 = math.sin(rad) * BARREL_RADIUS * 0.3
            x2 = math.cos(rad) * BARREL_RADIUS
            y2 = math.sin(rad) * BARREL_RADIUS
            canvas.drawLine(x1, y1, x2, y2, outline)

        band_y1 = -BARREL_RADIUS * 0.4
        canvas.drawLine(-BARREL_RADIUS, band_y1, BARREL_RADIUS, band_y1, outline)

        band_y2 = BARREL_RADIUS * 0.4
        canvas.drawLine(-BARREL_RADIUS, band_y2, BARREL_RADIUS, band_y2, outline)

    @classmethod
    def create(cls, rotation: Rotation = Rotation.ROT_0) -> 'Barrels':
        return cls((0, 0), rotation=rotation)
