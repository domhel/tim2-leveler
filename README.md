# TIM2 Leveler

A Python tool for creating and parsing The Incredible Machine 2/3 level files (`.TIM` format).

## Overview

This project provides a complete implementation for generating and analyzing TIM2/3 puzzle files. It includes data structures for all major part types, support for parsing existing levels, and a flexible API for creating new puzzles programmatically.

## Features

- **Level Generation**: Create TIM2/3 levels programmatically with Python
- **Level Parsing**: Parse and analyze existing `.TIM` files with detailed output
- **Format Conversion**: Convert between binary TIM and human-readable JSON formats
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

### Convert TIM to JSON

Convert a binary `.TIM` file to human-readable JSON format:

```bash
uv run main.py --tim2json path/to/level.TIM
```

This creates `level.json` in the same directory with:
- Human-readable part type names (e.g., "BOWLING_BALL" instead of 0)
- Flag names as string arrays (e.g., ["MOVING_PART", "CAN_FLIP_HORIZONTAL"])
- Structured data with clear field names
- Only non-default values included for cleaner output:
  - Size fields omitted for parts using default 32x32 dimensions
  - Unknown bytes that are always 0 are excluded
  - Empty sections (hints, solution) are omitted if not used

### Convert JSON to TIM

Convert a JSON file back to binary `.TIM` format:

```bash
uv run main.py --json2tim path/to/level.json
```

This creates `level.TIM` in the same directory. You can:
- Edit level properties in a text editor
- Modify part positions, types, and flags
- Add or remove parts
- Change global settings like gravity and music
- Then convert back to TIM format for use in the game

### Example JSON Format

```json
{
  "version": "TIM2",
  "title": "My Level",
  "description": "Complete the puzzle!",
  "background": {
    "color": 3
  },
  "global_settings": {
    "pressure": 67,
    "gravity": 272,
    "music": 1000
  },
  "parts": [
    {
      "part_type": "BOWLING_BALL",
      "flags_1": ["MOVING_PART"],
      "flags_2": [],
      "flags_3": ["UNKNOWN_0x8"],
      "position": {"x": 100, "y": 50}
    },
    {
      "part_type": "RED_BRICK_WALL",
      "flags_1": ["FIXED_PART_1", "FIXED_PART_2"],
      "flags_2": ["CAN_STRETCH_BOTH"],
      "flags_3": ["UNKNOWN_0x8", "WALL_PART"],
      "position": {"x": 50, "y": 300},
      "size": {
        "width_1": 500,
        "height_1": 32,
        "width_2": 500,
        "height_2": 32
      }
    }
  ]
}
```

**Note:** The bowling ball doesn't have a `size` field because it uses the default 32x32 dimensions. The wall has an explicit `size` because it's stretched to 500 pixels wide. Unknown fields that are always 0 are excluded from the JSON for clarity.

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

## JSON Format Benefits

The JSON conversion feature provides several advantages:

- **Human-readable**: Edit levels in any text editor
- **Version control friendly**: Text-based diffs show exactly what changed
- **Easy debugging**: See all part properties at a glance
- **Bulk editing**: Use scripts or text processing tools to modify levels
- **Documentation**: JSON files serve as self-documenting level descriptions
- **Cross-platform**: JSON is universally supported and easy to parse

## Acknowledgments

This project is based on the excellent reverse engineering work documented at:
https://moddingwiki.shikadi.net/wiki/The_Incredible_Machine_Level_Format

## License

See LICENSE file for details.