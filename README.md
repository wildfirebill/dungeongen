# DungeonGen

**Procedural dungeon map generator for tabletop RPGs** — generates hand-drawn-style dungeon layouts with rooms, passages, doors, water features, boss rooms, key shards, and safe rooms. Inspired by watabou's One Page Dungeon.

![Temple Dungeon](https://raw.githubusercontent.com/benjcooley/dungeongen/main/docs/dungeon_temple.png)

<p align="center">
  <a href="https://www.python.org/downloads/"><img alt="Python 3.10+" src="https://img.shields.io/badge/python-3.10%2B-blue?logo=python"/></a>
  <a href="LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/license-MIT-green"/></a>
  <a href="https://github.com/wildfirebill/dungeongen/releases"><img alt="GitHub Release" src="https://img.shields.io/github/v/release/wildfirebill/dungeongen"/></a>
  <a href="https://github.com/wildfirebill/dungeongen/issues"><img alt="GitHub Issues" src="https://img.shields.io/github/issues/wildfirebill/dungeongen"/></a>
</p>

---

## Features

### Procedural Layout Generation
- **Room placement** with configurable sizes and shapes (rectangular, circular) — generates 4 up to 150 rooms per dungeon
- **Intelligent passage routing** connecting rooms with organic hallways and corridors
- **Symmetry modes** — None, Bilateral (mirror symmetry), Radial (180°/90° rotational)
- **Configurable density** — Sparse, Normal, and Tight room packing
- **Automated doors** with open/closed states and locked doors
- **Stairs and dungeon exits** for multi-level mapping
- **Safe/respawn rooms** every 20 rooms marked with a portal icon
- **Boss rooms** with glowing borders and key-shard requirements
- **Key shard items** — collectibles scattered through side-branch rooms

### Hand-Drawn Map Rendering
- **Crosshatch shading** with organic linework for a hand-sketched aesthetic
- **Water features** — procedural pools, lakes, puddles with ripple effects and organic shorelines
- **Room decorations** — columns, altars, fountains, dais platforms, rocks, stars, podiums, curtains, barrels, coffins
- **High-quality output** — render to PNG or SVG at any resolution
- **Grid overlay** for tabletop role-playing game play
- **Map rotation** with auto-recomputed bounds

### Procedural Water System
- **Noise-based water generation** using marching squares with Chaikin curve smoothing
- **Depth levels** — Dry, Puddles, Pools, Lakes, Flooded
- **Organic shorelines** and ripple contour effects

---

## Demo

**150-room ULTIMATE dungeon** rendered with crosshatch shading and water features:

![150-room ULTIMATE Dungeon](https://raw.githubusercontent.com/wildfirebill/dungeongen/main/150room.png)

*Generate your own with `python -m dungeongen.webview.app` and select "ULTIMATE" size.*

---

## Quick Start

```bash
git clone https://github.com/wildfirebill/dungeongen.git
cd dungeongen
pip install -e .
python -m dungeongen.webview.app
```

Then open **http://localhost:5050** in your browser.

---

## Installation

### From Source

```bash
git clone https://github.com/wildfirebill/dungeongen.git
cd dungeongen
pip install -e .
```

### Requirements

- **Python** 3.10+
- **skia-python** — high-quality 2D rendering
- **numpy** — noise generation
- **Flask** — web preview interface
- **rich** — structured logging

---

## Usage

### Web Preview (GUI)

```bash
python -m dungeongen.webview.app
```

Opens an interactive web interface at http://localhost:5050 where you can configure dungeon size, symmetry, water depth, rotation, and room labels, then export as PNG or SVG.

### Python API (Programmatic)

```python
from dungeongen.layout import DungeonGenerator, GenerationParams, DungeonSize, SymmetryType
from dungeongen.webview.adapter import convert_dungeon
from dungeongen.map.water_layer import WaterDepth

params = GenerationParams()
params.size = DungeonSize.MEDIUM    # TINY to ULTIMATE (4-150 rooms)
params.symmetry = SymmetryType.BILATERAL

generator = DungeonGenerator(params)
dungeon = generator.generate(seed=42)

dungeon_map = convert_dungeon(dungeon, water_depth=WaterDepth.POOLS)
dungeon_map.render_to_png('my_dungeon.png')
dungeon_map.render_to_svg('my_dungeon.svg')
```

---

## Configuration

### Dungeon Sizes

| Size       | Rooms   | Use Case                     |
|------------|---------|------------------------------|
| TINY       | 4-6     | Quick one-shot, tutorial     |
| SMALL      | 6-10    | Short session dungeon        |
| MEDIUM     | 10-20   | Standard dungeon crawl       |
| LARGE      | 20-35   | Extended adventure           |
| XLARGE     | 35-50   | Large dungeon complex        |
| XXLARGE    | 50-75   | Mega-dungeon wing            |
| XXXLARGE   | 75-100  | Full mega-dungeon            |
| MEGA       | 100-125 | Massive dungeon              |
| ULTIMATE   | 125-150 | Maximum size dungeon         |

### Symmetry Types

| Type        | Description                       |
|-------------|-----------------------------------|
| `NONE`      | Fully asymmetric organic layout   |
| `BILATERAL` | Mirror symmetry (left/right)      |
| `RADIAL_2`  | 180° rotational symmetry          |
| `RADIAL_4`  | 90° rotational symmetry           |

### Water Depth

| Level      | Coverage | Description                   |
|------------|----------|-------------------------------|
| `DRY`      | 0%       | No water                     |
| `PUDDLES`  | ~45%     | Scattered shallow puddles    |
| `POOLS`    | ~65%     | Connected pool network       |
| `LAKES`    | ~82%     | Large lakes and waterways    |
| `FLOODED`  | ~90%     | Mostly flooded dungeon       |

---

## Project Structure

```
dungeongen/
├── src/dungeongen/      # Main Python package
│   ├── layout/          # Dungeon layout generation
│   │   ├── generator.py # Procedural generator (rooms, passages, doors)
│   │   ├── numbering.py # Longest-path-first DFS room numbering
│   │   ├── models.py    # Room, Passage, Door data models
│   │   ├── params.py    # Generation parameters and constraints
│   │   └── validator.py # Layout validation and debugging
│   │
│   ├── map/             # Map rendering engine
│   │   ├── map.py       # Main renderer (PNG/SVG output)
│   │   ├── room.py      # Room interior rendering and decorations
│   │   ├── passage.py   # Passage/corridor rendering
│   │   ├── water_layer.py # Procedural water generation
│   │   └── _props/      # Decoration props (columns, altars, etc.)
│   │
│   ├── drawing/         # Drawing utilities
│   │   ├── crosshatch.py    # Crosshatch shading engine
│   │   └── water.py         # Water and ripple rendering
│   │
│   ├── algorithms/      # Generic algorithms
│   │   ├── marching_squares.py  # Contour extraction
│   │   ├── chaikin.py          # Curve smoothing
│   │   └── poisson.py          # Poisson disk sampling
│   │
│   ├── graphics/        # Graphics primitives
│   │   ├── noise.py     # Perlin noise and FBM
│   │   └── shapes.py    # Shape primitives
│   │
│   └── webview/         # Web preview application
│       ├── app.py       # Flask web server
│       └── templates/   # HTML/CSS/JS templates
│
├── tests/               # Test suite
├── docs/                # Screenshots and documentation
├── debugger/            # Analysis and debugging tools
└── pyproject.toml       # Python package configuration
```

---

## Modifications by @wildfirebill

Fixes and enhancements to the original codebase:

- **Expanded dungeon sizes** — Added `XXLARGE` (50-75), `XXXLARGE` (75-100), `ULTIMATE` (125-150) tiers between XLARGE and MEGA
- **Safe/respawn rooms** — Every 20th room tagged as a safe room with portal icon, shown in both SVG layout view and Skia map render
- **Boss rooms & key shards** — Red border glow on boss rooms, diamond key-shard icons, locked door padlock overlay, boss key-requirement labels in the Skia/PNG render pipeline
- **Coordinate limit fixes** — Raised hardcoded limits (4200 → 12800 map units) so MEGA/ULTIMATE dungeons render without crashing
- **Auto-rotate transform** — Map rotation (0-360°) applied around center with auto-recomputed bounds
- **Room names & dungeon titles** — Deterministic room name generation from tags/seed/number, dungeon title from seed, rendered on the map
- **Webview UI** — Rotation control, room name toggle, dungeon title toggle

---

## Acknowledgments

This project was created by [**benjcooley**](https://github.com/benjcooley). Thanks for the excellent procedural generation and rendering engine.

### Inspiration

- [**watabou's One Page Dungeon**](https://watabou.itch.io/one-page-dungeon) — the hand-drawn crosshatch aesthetic and visual style draw heavily from watabou's work
- [**watabou's generators**](https://watabou.itch.io/) — more procedural content for tabletop RPGs

### Differences from One Page Dungeon

This is a complete Python rewrite, not a port. Options and behavior differ from the original. Notable gaps:

- Various edge cases and bugs remain — not everything works perfectly in every configuration

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

![Example Dungeon](https://raw.githubusercontent.com/benjcooley/dungeongen/main/docs/dungeon_example.png)
