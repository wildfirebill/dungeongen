"""Prop type definitions."""

from enum import StrEnum, auto
from typing import TYPE_CHECKING, Type

from dungeongen.graphics.rotation import Rotation

if TYPE_CHECKING:
    from dungeongen.map._props.prop import Prop # type: ignore
    from dungeongen.map._props.rock import Rock # type: ignore

class PropType(StrEnum):
    """Available prop types that can be added to map elements."""
    
    # Rock types
    SMALL_ROCK = auto()
    MEDIUM_ROCK = auto()
    LARGE_ROCK = auto()
    
    # Furniture
    ALTAR = auto()
    COFFIN = auto()
    ROUND_COLUMN = auto()
    SQUARE_COLUMN = auto() 
    DIAS = auto()
    
    # Decorations
    STAR = auto()
    PODIUM = auto()
    CURTAINS = auto()
    BARRELS = auto()
    
    @classmethod
    def rock_types(cls) -> list['PropType']:
        """Get all rock prop types."""
        return [cls.SMALL_ROCK, cls.MEDIUM_ROCK, cls.LARGE_ROCK]
        
    def create_prop(self, rotation: Rotation = Rotation.ROT_0) -> 'Prop':
        """Create a new prop instance of this type.
        
        Args:
            rotation: Optional rotation for the prop
            
        Returns:
            New prop instance
            
        Raises:
            ValueError: If prop type is not supported
        """
        if self == PropType.SMALL_ROCK:
            return Rock.create_small()
        elif self == PropType.MEDIUM_ROCK:
            return Rock.create_medium()
        elif self == PropType.LARGE_ROCK:
            return Rock.create_large()
        elif self == PropType.COFFIN:
            from dungeongen.map._props.coffin import Coffin, COFFIN_PROP_TYPE
            return Coffin(COFFIN_PROP_TYPE, (0, 0), rotation=rotation)
        elif self == PropType.STAR:
            from dungeongen.map._props.star import Star
            return Star((0, 0), rotation=rotation)
        elif self == PropType.PODIUM:
            from dungeongen.map._props.podium import Podium
            return Podium((0, 0), rotation=rotation)
        elif self == PropType.CURTAINS:
            from dungeongen.map._props.curtains import Curtains
            return Curtains((0, 0), rotation=rotation)
        elif self == PropType.BARRELS:
            from dungeongen.map._props.barrels import Barrels
            return Barrels((0, 0), rotation=rotation)
        else:
            raise ValueError(f"Unsupported prop type: {self}")
