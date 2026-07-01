"""Room and dungeon name generation."""

import random
from typing import List

_BOSS_NAMES = [
    "Boss Chamber", "Throne Room", "Overlord's Sanctum",
    "Lich's Domain", "Warden's Keep", "Shadow Throne",
    "Heart of Darkness", "The Pit", "Obsidian Hall",
]

_HUB_NAMES = [
    "Central Hub", "Crossroads", "Great Hall",
    "The Commons", "Gathering Place", "Nexus",
    "The Bazaar", "Meeting Hall", "Concord Chamber",
]

_LAIR_NAMES = [
    "The Lair", "Den of Beasts", "The Warren",
    "Feral Hollow", "Bestial Pit", "The Burrow",
    "Wild Den", "The Menagerie",
]

_SANCTUM_NAMES = [
    "Inner Sanctum", "Sacred Chamber", "The Sanctuary",
    "Hallowed Ground", "The Vault", "Consecrated Hall",
    "Tranquil Court", "Sealed Room",
]

_DEAD_END_NAMES = [
    "Dead End", "Cul-de-Sac", "The Brink",
    "Lonely Hall", "End of the Line", "The Precipice",
    "Last Stand", "Isolated Cell",
]

_ENTRANCE_NAMES = [
    "Entrance", "Entry Hall", "The Foyer",
    "Gatehouse", "Outer Keep", "The Threshold",
    "Portal Chamber", "Welcome Hall",
]

_DUNGEON_ADJECTIVES = [
    "Forgotten", "Crimson", "Sapphire", "Obsidian",
    "Ancient", "Sunken", "Forsaken", "Crystal",
    "Iron", "Shadow", "Golden", "Bone",
    "Ashen", "Violet", "Emerald", "Rust",
    "Frozen", "Shifting", "Silent", "Ivory",
]

_DUNGEON_NOUNS = [
    "Catacombs", "Depths", "Labyrinth", "Vaults",
    "Dungeons", "Caverns", "Halls", "Ruins",
    "Crypts", "Mines", "Chambers", "Maze",
    "Tunnels", "Sanctum", "Keep", "Citadel",
]

_ROOM_PREFIXES = [
    "Room", "Chamber", "Hall", "Cell", "Court", "Vault",
]

_ROOM_ADJECTIVES = [
    "Quiet", "Dim", "Echoing", "Narrow", "Vast",
    "Cold", "Warm", "Damp", "Dry", "Dark",
    "Hollow", "Deep", "High", "Low", "Strange",
]

_ROOM_NOUNS = [
    "Stone", "Ash", "Dust", "Rime", "Clay",
    "Flint", "Salt", "Moss", "Slate", "Ember",
    "Cinder", "Briar", "Thorn", "Drift", "Pine",
]


def generate_room_name(tags: List[str], number: int, seed: int) -> str:
    rng = random.Random(seed)

    if 'boss' in tags:
        return rng.choice(_BOSS_NAMES)

    if 'hub' in tags:
        return rng.choice(_HUB_NAMES)

    if 'lair' in tags:
        return rng.choice(_LAIR_NAMES)

    if 'sanctum' in tags:
        return rng.choice(_SANCTUM_NAMES)

    if 'dead_end' in tags and rng.random() < 0.7:
        return rng.choice(_DEAD_END_NAMES)

    if number == 1:
        return rng.choice(_ENTRANCE_NAMES)

    adj = rng.choice(_ROOM_ADJECTIVES)
    noun = rng.choice(_ROOM_NOUNS)
    suffix = rng.choice(_ROOM_PREFIXES)
    name = f"{adj} {noun} {suffix}"
    if rng.random() < 0.3:
        name = name.split(" ")[0] + " " + name.split(" ")[2]
    return name


def generate_dungeon_title(seed: int) -> str:
    rng = random.Random(seed)
    adj = rng.choice(_DUNGEON_ADJECTIVES)
    noun = rng.choice(_DUNGEON_NOUNS)
    return f"The {adj} {noun}"
