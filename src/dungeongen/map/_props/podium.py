"""Podium prop implementation."""

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

PODIUM_X = CELL_SIZE * -0.35
PODIUM_Y = CELL_SIZE * -0.35
PODIUM_WIDTH = CELL_SIZE * 0.7
PODIUM_HEIGHT = CELL_SIZE * 0.7

PODIUM_PROP_TYPE = PropType(
    is_grid_aligned=True,
    boundary_shape=Rectangle(PODIUM_X, PODIUM_Y, PODIUM_WIDTH, PODIUM_HEIGHT),
    grid_size=(1, 1)
)

class Podium(Prop):
    """A stepped rectangular platform with concentric tiers."""

    def __init__(self, position: Point, rotation: Rotation = Rotation.ROT_0) -> None:
        super().__init__(PODIUM_PROP_TYPE, position, rotation=rotation)

    def _draw_content(self, canvas: skia.Canvas, bounds: Rectangle, layer: Layers = Layers.PROPS) -> None:
        if layer != Layers.PROPS:
            return

        options = self._map.options if self._map else None
        stroke = options.prop_stroke_width if options else 2.0
        fill_color = options.prop_fill_color if options else 0xFFFFFFFF
        outline_color = options.prop_outline_color if options else 0xFF000000

        tiers = [1.0, 0.72, 0.5]
        for i, scale in enumerate(tiers):
            w = PODIUM_WIDTH * scale
            h = PODIUM_HEIGHT * scale
            inset_x = (PODIUM_WIDTH - w) / 2
            inset_y = (PODIUM_HEIGHT - h) / 2

            rect = Rectangle(
                PODIUM_X + inset_x,
                PODIUM_Y + inset_y,
                w, h
            )

            fill = skia.Paint(AntiAlias=True, Style=skia.Paint.kFill_Style, Color=fill_color)
            rect.draw(canvas, fill)

            sw = stroke * (1.5 if i == 0 else 1.0)
            outline = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=sw, Color=outline_color)
            rect.draw(canvas, outline)

    @classmethod
    def create(cls, rotation: Rotation = Rotation.ROT_0) -> 'Podium':
        return cls((0, 0), rotation=rotation)
