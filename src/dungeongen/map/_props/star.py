"""Star prop implementation."""

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

STAR_RADIUS = CELL_SIZE * 0.35

STAR_PROP_TYPE = PropType(
    is_grid_aligned=True,
    boundary_shape=Rectangle(-STAR_RADIUS, -STAR_RADIUS, STAR_RADIUS * 2, STAR_RADIUS * 2),
    grid_size=(1, 1)
)

class Star(Prop):
    """A 5-pointed star prop drawn as an outlined path."""

    def __init__(self, position: Point, rotation: Rotation = Rotation.ROT_0) -> None:
        super().__init__(STAR_PROP_TYPE, position, rotation=rotation)

    def _draw_content(self, canvas: skia.Canvas, bounds: Rectangle, layer: Layers = Layers.PROPS) -> None:
        if layer != Layers.PROPS:
            return

        options = self._map.options if self._map else None

        cx, cy = 0.0, 0.0
        outer = STAR_RADIUS
        inner = outer * 0.382

        path = skia.Path()
        for i in range(10):
            angle = -math.pi / 2 + i * math.pi / 5
            r = outer if i % 2 == 0 else inner
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            if i == 0:
                path.moveTo(x, y)
            else:
                path.lineTo(x, y)
        path.close()

        fill_paint = skia.Paint(
            AntiAlias=True,
            Style=skia.Paint.kFill_Style,
            Color=options.prop_fill_color if options else 0xFFFFFFFF
        )
        canvas.drawPath(path, fill_paint)

        outline_paint = skia.Paint(
            AntiAlias=True,
            Style=skia.Paint.kStroke_Style,
            StrokeWidth=options.prop_stroke_width if options else 2.0,
            Color=options.prop_outline_color if options else 0xFF000000
        )
        canvas.drawPath(path, outline_paint)

    @classmethod
    def create(cls, rotation: Rotation = Rotation.ROT_0) -> 'Star':
        return cls((0, 0), rotation=rotation)
