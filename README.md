# TIM2 Leveler

A Python tool for creating and parsing The Incredible Machine 2/3 level files (`.TIM` format).

## Overview

This project provides a complete implementation for generating and analyzing TIM2/3 puzzle files. It includes data structures for all major part types, support for parsing existing levels, and a flexible API for creating new puzzles programmatically.

## Features

- **Level Generation**: Create TIM2/3 levels programmatically with Python
- **Level Parsing**: Parse and analyze existing `.TIM` files with detailed output
- **Complete Part Support**: Data structures for all part types including:
  - Normal parts (bowling balls, basketballs, walls, etc.)
  - Belts (conveyor belts with connections)
  - Ropes (with segment lengths and connections)
  - Pulleys (with rope connection points)
  - Programmable balls (with physics properties)
- **Flag Enumerations**: Human-readable flag definitions for part properties
- **Configurable Settings**: Customize background colors, music, gravity, pressure, and more

## Installation

This project uses `uv` for dependency management. Install dependencies with:

```bash
uv sync
```

## Usage

### Generate a Level

Create a new level with custom parameters:

```bash
uv run main.py --title "My Level" --description "Complete the puzzle!" --output mylevel.TIM
```

#### Options:
- `--title TEXT`: Quiz title for the level (default: "My spiral test")
- `--description TEXT`: Goal description (default: "Press start and it will lag like hell!")
- `--output PATH`: Output file path (default: "SPIRAL.TIM")
- `--color INT`: Background color 0-16 (default: 3)
- `--music INT`: Music track 1000-1023 (default: 1000)
- `--debug`: Print hex dump of generated file

### Parse an Existing Level

Analyze a `.TIM` file to see all its components:

```bash
uv run main.py --parse path/to/level.TIM
```

This will display:
- Magic number and file validation
- Background color
- Quiz title and goal description
- Global puzzle settings (gravity, pressure, music, etc.)
- Detailed part information with positions, flags, and connections
- Solution conditions
- File statistics

### Example Output

```
Magic Number: 0xEFAC1301
Background: unknown=0, color=3
Quiz Title: 'My spiral test'
Goal Description: 'Press start and it will lag like hell!'

============================================================
Global Puzzle Information:
============================================================
  Pressure: 67
  Gravity: 272
  Music: 1000
  Fixed Parts: 0
  Moving Parts: 150

============================================================
Normal Parts (150):
============================================================

  Part 0: BOWLING_BALL
    Position: (320, 150)
    Size 1: 32 x 32
    Size 2: 32 x 32
    ...
```

## Programmatic Usage

You can use the library in your own Python code:

```python
from main import make_part, PartType, make_buffer

# Create parts
ball = make_part(PartType.BOWLING_BALL, x=100, y=50, moving=True)
wall = make_part(PartType.RED_BRICK_WALL, x=200, y=300, moving=False)

# Generate level file
buffer = make_buffer(
    color=3,
    music=1000,
    quiz_title=b"My Level\0",
    goal_description=b"Drop the ball!\0",
    normal_parts=[ball, wall],
    belts=[],
    ropes=[],
    pulleys=[],
)

# Save to file
with open('mylevel.TIM', 'wb') as f:
    f.write(buffer)
```

## File Format

TIM2/3 files follow this structure:

1. **Header**: Magic number (0xEFAC1301) and background color
2. **Strings**: Null-terminated quiz title and goal description
3. **Hints**: Hint count and hint data (8 slots)
4. **Global Info**: 16 bytes with pressure, gravity, music, part counts
5. **Parts**: Sequential part data (48-60 bytes per part depending on type)
6. **Solution**: 132 bytes describing win conditions

## Part Types

Over 100 part types are defined, including:

- **Balls**: Bowling ball, basketball, pool ball, super ball, programmable ball
- **Walls**: Red brick, wood, pipe, curved pipe, caution wall
- **Machines**: Conveyor belt, electric motor, vacuum, cannon, bike pump
- **Connectors**: Rope, belt, pulley, gear
- **Special**: Mel Schlemming, alligator, jack-in-the-box, fish tank
- **Lasers**: Green laser, blue laser, angled mirror, laser mixer
- **Scenery**: Trees, clouds, grass (parts 110+)

## Acknowledgments

This project is based on the excellent reverse engineering work documented at:
https://moddingwiki.shikadi.net/wiki/The_Incredible_Machine_Level_Format

## License

See LICENSE file for details.