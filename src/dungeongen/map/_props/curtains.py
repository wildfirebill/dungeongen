"""Curtains prop implementation."""

import math
import skia
from typing import TYPE_CHECKING

from dungeongen.graphics.shapes import Rectangle
from dungeongen.graphics.aliases import Point
from dungeongen.constants import CELL_SIZE
from dungeongen.map._props.prop import Prop, PropType
from dungeongen.map.enums import Layers
from dungeongen.graphics.rotation import Rotation

if TYPE_CHECKING:
    from dungeongen.map.map import Map

CURTAIN_WIDTH = CELL_SIZE * 0.7
CURTAIN_HEIGHT = CELL_SIZE * 0.85
CURTAIN_X = -CURTAIN_WIDTH / 2
CURTAIN_Y = -CURTAIN_HEIGHT / 2

CURTAINS_PROP_TYPE = PropType(
    is_wall_aligned=True,
    is_grid_aligned=True,
    boundary_shape=Rectangle(CURTAIN_X, CURTAIN_Y, CURTAIN_WIDTH, CURTAIN_HEIGHT),
    grid_size=(1, 1)
)

class Curtains(Prop):
    """Wall-aligned draped fabric shapes with wavy bottom edge."""

    def __init__(self, position: Point, rotation: Rotation = Rotation.ROT_0) -> None:
        super().__init__(CURTAINS_PROP_TYPE, position, rotation=rotation)

    def _draw_content(self, canvas: skia.Canvas, bounds: Rectangle, layer: Layers = Layers.PROPS) -> None:
        if layer != Layers.PROPS:
            return

        options = self._map.options if self._map else None
        stroke = options.prop_stroke_width if options else 2.0
        fill_color = options.prop_fill_color if options else 0xFFFFFFFF
        outline_color = options.prop_outline_color if options else 0xFF000000

        w = CURTAIN_WIDTH
        h = CURTAIN_HEIGHT

        path = skia.Path()
        path.moveTo(CURTAIN_X, CURTAIN_Y)
        path.lineTo(CURTAIN_X + w, CURTAIN_Y)
        path.lineTo(CURTAIN_X + w, CURTAIN_Y + h * 0.6)

        segments = 8
        seg_w = w / segments
        for i in range(segments + 1):
            px = CURTAIN_X + i * seg_w
            t = i / segments
            wave = math.sin(t * math.pi * 1.5) * h * 0.08
            py = CURTAIN_Y + h * 0.6 + wave
            if i == 0:
                path.lineTo(px, py)
            else:
                path.lineTo(px, py)

        path.lineTo(CURTAIN_X, CURTAIN_Y + h * 0.6)
        path.close()

        fill = skia.Paint(AntiAlias=True, Style=skia.Paint.kFill_Style, Color=fill_color)
        canvas.drawPath(path, fill)

        outline = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=stroke, Color=outline_color)
        canvas.drawPath(path, outline)

        tie_x = CURTAIN_X + w * 0.25
        tie_w = w * 0.08
        tie_rect = Rectangle(tie_x, CURTAIN_Y + h * 0.45, tie_w, h * 0.15)
        tie_fill = skia.Paint(AntiAlias=True, Style=skia.Paint.kFill_Style, Color=fill_color)
        tie_rect.draw(canvas, tie_fill)
        tie_rect.draw(canvas, outline)

        tie2_x = CURTAIN_X + w * 0.67
        tie2_rect = Rectangle(tie2_x, CURTAIN_Y + h * 0.45, tie_w, h * 0.15)
        tie2_rect.draw(canvas, tie_fill)
        tie2_rect.draw(canvas, outline)

    @classmethod
    def create(cls, rotation: Rotation = Rotation.ROT_0) -> 'Curtains':
        return cls((0, 0), rotation=rotation)
