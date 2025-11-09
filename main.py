import struct
import math
import argparse
import json
from pathlib import Path
from enum import IntEnum, IntFlag
from dataclasses import dataclass


class PartType(IntEnum):
    """Part type numbers for TIM2/3"""
    BOWLING_BALL = 0
    RED_BRICK_WALL = 1
    WOOD_INCLINE = 2
    TIPSY_TRAILER = 3
    BALLOON = 4
    CONVEYOR_BELT = 5
    MOUSE_MOTOR = 6
    PULLEY = 7
    BELT = 8
    BASKETBALL = 9
    ROPE = 10
    LAUNDRY_BASKET = 11
    CURIE_CAT = 12
    JACK_IN_THE_BOX = 13
    GEAR = 14
    FISH_TANK = 15
    BIKE_PUMP = 16
    BUCKET = 17
    CANNON = 18
    # 19-45 not listed in source
    PIPE_WALL = 46
    CURVED_PIPE_WALL = 47
    WOOD_WALL = 48
    ROPE_END_PHANTOM = 49
    ELECTRIC_MOTOR = 50
    VACUUM = 51
    CHEESE = 52
    THUMB_TACK = 53
    MEL_SCHLEMMING = 54
    REMOTE_CONTROL_EXPLOSIVES = 55
    CAUTION_WALL = 56
    LARGE_CURVED_PIPE = 57
    MELS_HOUSE = 58
    SUPER_BALL = 59
    GRASS_FLOOR = 60
    ALLIGATOR = 61
    COFFEE_POT = 62
    POOL_BALL = 63
    PINBALL_BUMPER = 64
    # 65-75 not listed in source
    STEEL_CABLE = 76
    # 77-86 not listed in source
    PROGRAMMABLE_BALL = 87
    # 88-91 not listed in source
    GREEN_LASER = 92
    BLUE_LASER = 93
    ANGLED_MIRROR = 94
    LASER_MIXER = 95
    LASER_ACTIVATED_PLUG = 96
    LARGE_PIPES = 97
    T_CONNECTOR = 98
    GRASS_INCLINE = 99
    LOG_INCLINE = 100
    GRANITE_INCLINE = 101
    BRICK_INCLINE = 102
    ARCHWAY = 103
    WOODEN_BARRIER = 104
    SCAFFOLD_BARRIER = 105
    LATTICE_ARCHWAY = 106
    ELECTRIC_MIXER = 107
    LEAKY_BUCKET = 108
    BLIMP = 109
    # 110+ are scenery parts (trees, clouds, etc.)


class Flags1(IntFlag):
    """Flags for TIM2/3 parts (flags_1)"""
    UNKNOWN_0x40 = 0x40  # Used for moving parts, not always set
    CAN_FLIP_VERTICAL = 0x200
    CAN_FLIP_HORIZONTAL = 0x400
    MOVING_PART = 0x1000  # Moving part, affected by gravity
    FIXED_PART_1 = 0x2000  # Used in combination with FIXED_PART_2
    FIXED_PART_2 = 0x4000  # Parts that don't move and aren't affected by gravity


class Flags2(IntFlag):
    """Flags for parts (flags_2)"""
    BELT_CAN_CONNECT = 0x1
    BELT_IS_CONNECTED = 0x2
    ROPE_CAN_CONNECT = 0x4
    ROPE_CAN_CONNECT_2 = 0x8  # Second rope (teeter-totter)
    SPRITE_FLIP_HORIZONTAL = 0x10
    SPRITE_FLIP_VERTICAL = 0x20
    PROBABLY_UNUSED = 0x40
    CAN_STRETCH_ONE_DIR = 0x80  # Inclines, conveyor belt, walls
    CAN_STRETCH_BOTH = 0x100  # Walls


class Flags3(IntFlag):
    """Flags for TIM2/3 parts (flags_3)"""
    CAN_PLUG_OUTLET = 0x1
    IS_ELECTRIC_OUTLET = 0x2
    CAN_BURN_OR_FUSE = 0x4  # Candle, dynamite, cannon
    UNKNOWN_0x8 = 0x8
    LOCKED = 0x40  # Not placed in parts bin
    SIZABLE_SCENERY = 0x80
    UNKNOWN_0x100 = 0x100
    SHOW_PROGRAM_ICON = 0x400
    SCENERY_PART = 0x1000
    WALL_PART = 0x2000
    SHOW_SOLUTION_ICON = 0x8000


def get_default_part_size(part_type: PartType) -> tuple[int, int, int, int]:
    """Get default size for a part type (width_1, height_1, width_2, height_2)"""
    # Most parts are 32x32 by default
    # Add specific sizes here as they are discovered
    return (0x20, 0x20, 0x20, 0x20)


@dataclass
class Part:
    """Base class for normal parts (48 bytes)"""
    part_type: PartType
    flags_1: int = 0
    flags_2: int = 0
    flags_3: int = 0
    appearance: int = 0
    unknown_10: int = 0
    width_1: int = 0x20
    height_1: int = 0x20
    width_2: int = 0x20
    height_2: int = 0x20
    pos_x: int = 0
    pos_y: int = 0
    behavior: int = 0
    unknown_26: int = 0
    belt_connect_pos_x: int = 0
    belt_connect_pos_y: int = 0
    belt_line_distance: int = 0
    unknown_32: int = 0
    rope_1_connect_pos_x: int = 0
    rope_1_connect_pos_y: int = 0
    unknown_36: int = 0
    rope_2_connect_pos_x: int = 0
    rope_2_connect_pos_y: int = 0
    connected_1: int = -1
    connected_2: int = -1
    outlet_plugged_1: int = -1
    outlet_plugged_2: int = -1

    def to_bytes(self) -> bytes:
        """Pack the part data into 48 bytes"""
        return struct.pack(
            '<HHHHHHHHHHhhHHBBHHBBHBBhhhh',
            self.part_type, self.flags_1, self.flags_2, self.flags_3,
            self.appearance, self.unknown_10,
            self.width_1, self.height_1, self.width_2, self.height_2,
            self.pos_x, self.pos_y,
            self.behavior, self.unknown_26,
            self.belt_connect_pos_x, self.belt_connect_pos_y,
            self.belt_line_distance, self.unknown_32,
            self.rope_1_connect_pos_x, self.rope_1_connect_pos_y,
            self.unknown_36,
            self.rope_2_connect_pos_x, self.rope_2_connect_pos_y,
            self.connected_1, self.connected_2,
            self.outlet_plugged_1, self.outlet_plugged_2
        )

    @classmethod
    def from_bytes(cls, data: bytes, offset: int = 0) -> 'Part':
        """Unpack 48 bytes into a Part object"""
        values = struct.unpack_from('<HHHHHHHHHHhhHHBBHHBBHBBhhhh', data, offset)
        return cls(
            part_type=PartType(values[0]),
            flags_1=values[1],
            flags_2=values[2],
            flags_3=values[3],
            appearance=values[4],
            unknown_10=values[5],
            width_1=values[6],
            height_1=values[7],
            width_2=values[8],
            height_2=values[9],
            pos_x=values[10],
            pos_y=values[11],
            behavior=values[12],
            unknown_26=values[13],
            belt_connect_pos_x=values[14],
            belt_connect_pos_y=values[15],
            belt_line_distance=values[16],
            unknown_32=values[17],
            rope_1_connect_pos_x=values[18],
            rope_1_connect_pos_y=values[19],
            unknown_36=values[20],
            rope_2_connect_pos_x=values[21],
            rope_2_connect_pos_y=values[22],
            connected_1=values[23],
            connected_2=values[24],
            outlet_plugged_1=values[25],
            outlet_plugged_2=values[26],
        )


@dataclass
class Belt(Part):
    """Belt part (52 bytes)"""
    unknown_28: int = 0
    unknown_30: int = 0
    belt_connected_part_1: int = -1
    belt_connected_part_2: int = -1
    unknown_36_belt: int = 0
    unknown_38: int = 0
    unknown_40: int = 0
    unknown_42: int = 0

    def to_bytes(self) -> bytes:
        """Pack the belt data into 52 bytes"""
        base = struct.pack(
            '<HHHHHHHHHHhhHHHHhhHHHH',
            self.part_type, self.flags_1, self.flags_2, self.flags_3,
            self.appearance, self.unknown_10,
            self.width_1, self.height_1, self.width_2, self.height_2,
            self.pos_x, self.pos_y,
            self.behavior, self.unknown_26,
            self.unknown_28, self.unknown_30,
            self.belt_connected_part_1, self.belt_connected_part_2,
            self.unknown_36_belt, self.unknown_38, self.unknown_40, self.unknown_42
        )
        # Add the standard ending fields
        ending = struct.pack('<hhhh', 
            self.connected_1, self.connected_2,
            self.outlet_plugged_1, self.outlet_plugged_2
        )
        return base + ending


@dataclass
class Rope(Part):
    """Rope part (54 bytes)"""
    rope_segment_length: int = 0
    unknown_28: int = 0
    unknown_30: int = 0
    unknown_32_rope: int = 1
    rope_connected_part_1: int = -1
    rope_connected_part_2: int = -1
    part_1_connect_field_usage: int = 0
    part_2_connect_field_usage: int = 0
    unknown_44: int = 0
    unknown_46: int = 0

    def to_bytes(self) -> bytes:
        """Pack the rope data into 54 bytes"""
        base = struct.pack(
            '<HHHHHHHHHHhhHHHHHHhhBBHH',
            self.part_type, self.flags_1, self.flags_2, self.flags_3,
            self.appearance, self.unknown_10,
            self.width_1, self.height_1, self.width_2, self.height_2,
            self.pos_x, self.pos_y,
            self.rope_segment_length, self.unknown_26,
            self.unknown_28, self.unknown_30, self.unknown_32_rope,
            self.unknown_36,
            self.rope_connected_part_1, self.rope_connected_part_2,
            self.part_1_connect_field_usage, self.part_2_connect_field_usage,
            self.unknown_44, self.unknown_46
        )
        # Add the standard ending fields
        ending = struct.pack('<hhhh',
            self.connected_1, self.connected_2,
            self.outlet_plugged_1, self.outlet_plugged_2
        )
        return base + ending


@dataclass
class Pulley(Part):
    """Pulley part (56 bytes)"""
    unknown_28: int = 0
    unknown_30: int = 0
    unknown_32_pulley: int = 1
    pulley_rope_1_connect_pos_x: int = 0
    pulley_rope_1_connect_pos_y: int = 0
    unknown_36_pulley: int = -1
    unknown_38: int = -1
    unknown_40: int = 0
    unknown_42: int = 0
    pulley_rope_2_connect_pos_x: int = 0
    pulley_rope_2_connect_pos_y: int = 0
    pulley_connected_1: int = -1
    pulley_connected_2: int = -1
    unknown_50: int = -1
    unknown_52: int = -1
    rope_index: int = -1

    def to_bytes(self) -> bytes:
        """Pack the pulley data into 56 bytes"""
        return struct.pack(
            '<HHHHHHHHHHhhHHHHHBBhhHHBBhhhh',
            self.part_type, self.flags_1, self.flags_2, self.flags_3,
            self.appearance, self.unknown_10,
            self.width_1, self.height_1, self.width_2, self.height_2,
            self.pos_x, self.pos_y,
            self.behavior, self.unknown_26,
            self.unknown_28, self.unknown_30, self.unknown_32_pulley,
            self.pulley_rope_1_connect_pos_x, self.pulley_rope_1_connect_pos_y,
            self.unknown_36_pulley, self.unknown_38,
            self.unknown_40, self.unknown_42,
            self.pulley_rope_2_connect_pos_x, self.pulley_rope_2_connect_pos_y,
            self.pulley_connected_1, self.pulley_connected_2,
            self.unknown_50, self.unknown_52,
            self.rope_index
        )


@dataclass
class ProgrammableBall(Part):
    """Programmable ball part (60 bytes)"""
    density: int = 2832
    elasticity: int = 128
    friction: int = 16
    gravity_buoyancy: int = 269
    mass: int = 200
    appearance_2: int = 0

    def to_bytes(self) -> bytes:
        """Pack the programmable ball data into 60 bytes"""
        base = super().to_bytes()
        extra = struct.pack('<HHHHHH',
            self.density, self.elasticity, self.friction,
            self.gravity_buoyancy, self.mass, self.appearance_2
        )
        return base + extra


def make_part(part_type: PartType, x: int = 0, y: int = 0, moving: bool = True) -> Part:
    """
    Create a part with sensible defaults based on type.
    
    Args:
        part_type: The type of part to create
        x: X position (0-560 for TIM2)
        y: Y position (0-377 for TIM2)
        moving: Whether the part is affected by gravity (moving parts)
    
    Returns:
        A Part object (or subclass) with appropriate defaults
    """
    # Common defaults for TIM2
    flags_1 = Flags1.MOVING_PART if moving else (Flags1.FIXED_PART_1 | Flags1.FIXED_PART_2)
    flags_2 = 0
    flags_3 = Flags3.UNKNOWN_0x8  # Common flag for many parts
    
    if part_type == PartType.BOWLING_BALL:
        return Part(
            part_type=part_type,
            flags_1=flags_1,
            flags_2=flags_2,
            flags_3=flags_3,
            width_1=0x20, height_1=0x20,
            width_2=0x20, height_2=0x20,
            pos_x=x, pos_y=y,
        )
    
    elif part_type == PartType.BASKETBALL:
        return Part(
            part_type=part_type,
            flags_1=flags_1,
            flags_2=flags_2,
            flags_3=flags_3,
            width_1=0x20, height_1=0x20,
            width_2=0x20, height_2=0x20,
            pos_x=x, pos_y=y,
        )
    
    elif part_type == PartType.BELT:
        return Belt(
            part_type=part_type,
            flags_1=Flags1.FIXED_PART_1 | Flags1.FIXED_PART_2,
            flags_2=0,
            flags_3=Flags3.LOCKED if not moving else 0,
            appearance=0,
            pos_x=-1, pos_y=-1,
            unknown_26=1,
        )
    
    elif part_type == PartType.ROPE:
        return Rope(
            part_type=part_type,
            flags_1=Flags1.FIXED_PART_1 | Flags1.FIXED_PART_2,
            flags_2=0,
            flags_3=Flags3.LOCKED if not moving else 0,
            appearance=0,
            pos_x=-1, pos_y=-1,
            unknown_32_rope=1,
        )
    
    elif part_type == PartType.PULLEY:
        return Pulley(
            part_type=part_type,
            flags_1=Flags1.FIXED_PART_1 | Flags1.FIXED_PART_2,
            flags_2=Flags2.ROPE_CAN_CONNECT,
            flags_3=(Flags3.LOCKED | Flags3.UNKNOWN_0x8) if not moving else Flags3.UNKNOWN_0x8,
            appearance=0,
            width_1=0x20, height_1=0x20,
            width_2=0x20, height_2=0x20,
            pos_x=x, pos_y=y,
            unknown_32_pulley=1,
        )
    
    elif part_type == PartType.PROGRAMMABLE_BALL:
        return ProgrammableBall(
            part_type=part_type,
            flags_1=flags_1,
            flags_2=flags_2,
            flags_3=flags_3 | Flags3.SHOW_PROGRAM_ICON,
            width_1=0x20, height_1=0x20,
            width_2=0x20, height_2=0x20,
            pos_x=x, pos_y=y,
        )
    
    else:
        # Generic part with defaults
        return Part(
            part_type=part_type,
            flags_1=flags_1,
            flags_2=flags_2,
            flags_3=flags_3,
            width_1=0x20, height_1=0x20,
            width_2=0x20, height_2=0x20,
            pos_x=x, pos_y=y,
        )


def insert_bowlingball(buffer, offset, x, y) -> int:
    """Legacy function - creates a bowling ball part using the new data structures"""
    assert 0 <= x <= 560
    assert 0 <= y <= 377
    
    ball = make_part(PartType.BOWLING_BALL, x, y, moving=True)
    buffer[offset:offset+48] = ball.to_bytes()
    return offset + 48

def calculate_filesize(title_length: int, description_length: int, num_normal_parts: int, num_belts: int, num_ropes: int, num_pulleys: int, num_programmable_balls: int) -> int:
    '''
    Returns the expected file size. Note that no hints are allowed currently.

    Title and description must be null-terminated and \0 included in their length.
    '''
    elements = {
        'magic': 4,
        'color': 2,
        'title': title_length,
        'description': description_length,
        'hints': 2 + 7 * 8, #2 byte num hints, (7 byte per empty hint (x_u16,y_u16,flip_u16,text\0)), 8 hints even if empty
        'global_puzzle_info': 16,
        'normal_parts': num_normal_parts * 48,
        'belts': num_belts * 52,
        'ropes': num_ropes * 54,
        'pulleys': num_pulleys * 56,
        'programmable_balls': num_programmable_balls * 60,
        'puzzle_solution_information': 132,
    }
    return sum(elements.values())

def calculate_num_parts(normal_parts: list, belts: list, ropes: list, pulleys: list) -> tuple[int,int]:
    # TODO: actually parse them to check moving flags
    num_fixed_parts = len(belts) + len(ropes) + len(pulleys)
    num_moving_parts = len(normal_parts)
    return num_fixed_parts, num_moving_parts
    
def make_buffer(color: int, music: int, quiz_title: bytes, goal_description: bytes, normal_parts: list, belts: list, ropes: list, pulleys: list) -> bytearray:
    assert 0 <= color <= 16
    assert 1000 <= music <= 1023

    quiz_title_len=len(quiz_title)
    goal_description_len=len(goal_description)
    num_fixed_parts, num_moving_parts = calculate_num_parts(normal_parts, belts, ropes, pulleys)
    filesize = calculate_filesize(quiz_title_len, goal_description_len, len(normal_parts), len(belts), len(ropes), len(pulleys), 0)
    buffer=bytearray(filesize)
    offset=0

    #Magic number
    struct.pack_into('>I', buffer, offset, 0xEFAC1301)
    offset+=4

    #Background
    struct.pack_into('>BB', buffer, offset, 0, color)
    offset+=2

    #Quiz title
    struct.pack_into(f'<{quiz_title_len}s', buffer, offset, quiz_title)
    offset+=quiz_title_len

    #Goal description
    struct.pack_into(f'<{goal_description_len}s', buffer, offset, goal_description)
    offset+=goal_description_len

    #Hints. 2 byte num hints, (7 byte per empty hint (x_u16,y_u16,flip_u16,text\0)), 8 hints even if empty
    hints_bytes_skip=2+7*8
    offset+=hints_bytes_skip

    #Global puzzle information
    pressure_i16 = 67
    gravity_i16 = 272
    unknown_4_u16 = unknown_6_u16 = 0
    music_u16 = music #1000-1023
    num_parts_fixed_u16 = num_fixed_parts
    num_parts_moving_u16 = num_moving_parts
    unknown_14_u16 = 0
    struct.pack_into('<hhHHHHHH', buffer, offset, pressure_i16, gravity_i16, unknown_4_u16, unknown_6_u16, music_u16, num_parts_fixed_u16, num_parts_moving_u16, unknown_14_u16)
    offset+=16

    #Basket Ball
    for i in range(num_moving_parts):
        num_rounds = 3
        angle = i / num_moving_parts * 2 * math.pi * num_rounds
        radius_min = 20
        radius_max = 150
        center_x = 300
        center_y = 150
        radius = int(radius_min + (radius_max - radius_min) * (i / num_moving_parts))
        x = int(center_x + radius * math.cos(angle))
        y = int(center_y + radius * math.sin(angle))
        match i % 4:
            case 0:
                part_type = PartType.BOWLING_BALL
            case 1:
                part_type = PartType.BASKETBALL
            case 2:
                part_type = PartType.POOL_BALL
            case _:
                part_type = PartType.SUPER_BALL
        ball = make_part(part_type, x, y, moving=True)
        ball_bytes = ball.to_bytes()
        buffer[offset:offset+len(ball_bytes)] = ball_bytes
        offset += len(ball_bytes)

    #Solution Information (132 bytes) u16 num, 8 entries * 16 byte each
    num_solution_conditions_u16 = 0
    struct.pack_into('<H', buffer, offset, num_solution_conditions_u16)
    offset+=2
    for _ in range(8):
        part_index_i16 = -1
        part_state_1_u16 = 0
        part_state_2_u16 = 0
        part_count_u16 = 0
        position_rect_x_i16 = 0
        position_rect_y_i16 = 0
        position_rect_width_i16 = 0
        position_rect_height_i16 = 0
        struct.pack_into('<hHHHhhhh', buffer, offset, part_index_i16, part_state_1_u16, part_state_2_u16, part_count_u16, position_rect_x_i16, position_rect_y_i16, position_rect_width_i16, position_rect_height_i16)
        offset+=16
    delay_u16 = 0
    struct.pack_into('<H', buffer, offset, delay_u16)
    offset+=2

    assert offset == len(buffer), f'{offset}, {len(buffer)}'

    return buffer
    

def flags1_to_list(flags: int) -> list[str]:
    """Convert Flags1 to list of flag names"""
    result = []
    if flags & Flags1.UNKNOWN_0x40:
        result.append("UNKNOWN_0x40")
    if flags & Flags1.CAN_FLIP_VERTICAL:
        result.append("CAN_FLIP_VERTICAL")
    if flags & Flags1.CAN_FLIP_HORIZONTAL:
        result.append("CAN_FLIP_HORIZONTAL")
    if flags & Flags1.MOVING_PART:
        result.append("MOVING_PART")
    if flags & Flags1.FIXED_PART_1:
        result.append("FIXED_PART_1")
    if flags & Flags1.FIXED_PART_2:
        result.append("FIXED_PART_2")
    return result

def flags2_to_list(flags: int) -> list[str]:
    """Convert Flags2 to list of flag names"""
    result = []
    if flags & Flags2.BELT_CAN_CONNECT:
        result.append("BELT_CAN_CONNECT")
    if flags & Flags2.BELT_IS_CONNECTED:
        result.append("BELT_IS_CONNECTED")
    if flags & Flags2.ROPE_CAN_CONNECT:
        result.append("ROPE_CAN_CONNECT")
    if flags & Flags2.ROPE_CAN_CONNECT_2:
        result.append("ROPE_CAN_CONNECT_2")
    if flags & Flags2.SPRITE_FLIP_HORIZONTAL:
        result.append("SPRITE_FLIP_HORIZONTAL")
    if flags & Flags2.SPRITE_FLIP_VERTICAL:
        result.append("SPRITE_FLIP_VERTICAL")
    if flags & Flags2.PROBABLY_UNUSED:
        result.append("PROBABLY_UNUSED")
    if flags & Flags2.CAN_STRETCH_ONE_DIR:
        result.append("CAN_STRETCH_ONE_DIR")
    if flags & Flags2.CAN_STRETCH_BOTH:
        result.append("CAN_STRETCH_BOTH")
    return result

def flags3_to_list(flags: int) -> list[str]:
    """Convert Flags3 to list of flag names"""
    result = []
    if flags & Flags3.CAN_PLUG_OUTLET:
        result.append("CAN_PLUG_OUTLET")
    if flags & Flags3.IS_ELECTRIC_OUTLET:
        result.append("IS_ELECTRIC_OUTLET")
    if flags & Flags3.CAN_BURN_OR_FUSE:
        result.append("CAN_BURN_OR_FUSE")
    if flags & Flags3.UNKNOWN_0x8:
        result.append("UNKNOWN_0x8")
    if flags & Flags3.LOCKED:
        result.append("LOCKED")
    if flags & Flags3.SIZABLE_SCENERY:
        result.append("SIZABLE_SCENERY")
    if flags & Flags3.UNKNOWN_0x100:
        result.append("UNKNOWN_0x100")
    if flags & Flags3.SHOW_PROGRAM_ICON:
        result.append("SHOW_PROGRAM_ICON")
    if flags & Flags3.SCENERY_PART:
        result.append("SCENERY_PART")
    if flags & Flags3.WALL_PART:
        result.append("WALL_PART")
    if flags & Flags3.SHOW_SOLUTION_ICON:
        result.append("SHOW_SOLUTION_ICON")
    return result

def list_to_flags1(flags_list: list[str]) -> int:
    """Convert list of flag names to Flags1 value"""
    flags = 0
    for flag_name in flags_list:
        if hasattr(Flags1, flag_name):
            flags |= getattr(Flags1, flag_name)
    return flags

def list_to_flags2(flags_list: list[str]) -> int:
    """Convert list of flag names to Flags2 value"""
    flags = 0
    for flag_name in flags_list:
        if hasattr(Flags2, flag_name):
            flags |= getattr(Flags2, flag_name)
    return flags

def list_to_flags3(flags_list: list[str]) -> int:
    """Convert list of flag names to Flags3 value"""
    flags = 0
    for flag_name in flags_list:
        if hasattr(Flags3, flag_name):
            flags |= getattr(Flags3, flag_name)
    return flags

def part_to_dict(part: Part) -> dict:
    """Convert a Part object to a JSON-serializable dictionary"""
    result = {
        "part_type": part.part_type.name,
        "flags_1": flags1_to_list(part.flags_1),
        "flags_2": flags2_to_list(part.flags_2),
        "flags_3": flags3_to_list(part.flags_3),
        "position": {"x": part.pos_x, "y": part.pos_y}
    }
    
    # Only include size if it differs from default
    default_w1, default_h1, default_w2, default_h2 = get_default_part_size(part.part_type)
    if (part.width_1 != default_w1 or part.height_1 != default_h1 or 
        part.width_2 != default_w2 or part.height_2 != default_h2):
        result["size"] = {
            "width_1": part.width_1,
            "height_1": part.height_1,
            "width_2": part.width_2,
            "height_2": part.height_2
        }
    
    # Add optional fields only if non-default (skip unknown_* fields that are 0)
    if part.appearance != 0:
        result["appearance"] = part.appearance
    if part.behavior != 0:
        result["behavior"] = part.behavior
    
    # Belt connections
    if part.belt_connect_pos_x != 0 or part.belt_connect_pos_y != 0 or part.belt_line_distance != 0:
        result["belt_connection"] = {
            "x": part.belt_connect_pos_x,
            "y": part.belt_connect_pos_y,
            "distance": part.belt_line_distance
        }
    
    # Rope connections
    if part.rope_1_connect_pos_x != 0 or part.rope_1_connect_pos_y != 0:
        result["rope_1_connection"] = {
            "x": part.rope_1_connect_pos_x,
            "y": part.rope_1_connect_pos_y
        }
    if part.rope_2_connect_pos_x != 0 or part.rope_2_connect_pos_y != 0:
        result["rope_2_connection"] = {
            "x": part.rope_2_connect_pos_x,
            "y": part.rope_2_connect_pos_y
        }
    
    # Connected parts
    if part.connected_1 != -1:
        result["connected_1"] = part.connected_1
    if part.connected_2 != -1:
        result["connected_2"] = part.connected_2
    if part.outlet_plugged_1 != -1:
        result["outlet_plugged_1"] = part.outlet_plugged_1
    if part.outlet_plugged_2 != -1:
        result["outlet_plugged_2"] = part.outlet_plugged_2
    
    # Type-specific fields
    if isinstance(part, Belt):
        belt_data = {}
        if part.unknown_28 != 0:
            belt_data["unknown_28"] = part.unknown_28
        if part.unknown_30 != 0:
            belt_data["unknown_30"] = part.unknown_30
        if part.belt_connected_part_1 != -1:
            belt_data["connected_part_1"] = part.belt_connected_part_1
        if part.belt_connected_part_2 != -1:
            belt_data["connected_part_2"] = part.belt_connected_part_2
        if part.unknown_36_belt != 0:
            belt_data["unknown_36"] = part.unknown_36_belt
        if part.unknown_38 != 0:
            belt_data["unknown_38"] = part.unknown_38
        if part.unknown_40 != 0:
            belt_data["unknown_40"] = part.unknown_40
        if part.unknown_42 != 0:
            belt_data["unknown_42"] = part.unknown_42
        if belt_data:  # Only add if there's data
            result["belt_data"] = belt_data
    elif isinstance(part, Rope):
        rope_data = {}
        if part.rope_segment_length != 0:
            rope_data["segment_length"] = part.rope_segment_length
        if part.unknown_28 != 0:
            rope_data["unknown_28"] = part.unknown_28
        if part.unknown_30 != 0:
            rope_data["unknown_30"] = part.unknown_30
        if part.unknown_32_rope != 1:  # Default is 1, not 0
            rope_data["unknown_32"] = part.unknown_32_rope
        if part.rope_connected_part_1 != -1:
            rope_data["connected_part_1"] = part.rope_connected_part_1
        if part.rope_connected_part_2 != -1:
            rope_data["connected_part_2"] = part.rope_connected_part_2
        if part.part_1_connect_field_usage != 0:
            rope_data["part_1_connect_field_usage"] = part.part_1_connect_field_usage
        if part.part_2_connect_field_usage != 0:
            rope_data["part_2_connect_field_usage"] = part.part_2_connect_field_usage
        if part.unknown_44 != 0:
            rope_data["unknown_44"] = part.unknown_44
        if part.unknown_46 != 0:
            rope_data["unknown_46"] = part.unknown_46
        if rope_data:  # Only add if there's data
            result["rope_data"] = rope_data
    elif isinstance(part, Pulley):
        pulley_data: dict[str, object] = {}
        if part.unknown_28 != 0:
            pulley_data["unknown_28"] = part.unknown_28
        if part.unknown_30 != 0:
            pulley_data["unknown_30"] = part.unknown_30
        if part.unknown_32_pulley != 1:  # Default is 1, not 0
            pulley_data["unknown_32"] = part.unknown_32_pulley
        if (part.pulley_rope_1_connect_pos_x != 0 or part.pulley_rope_1_connect_pos_y != 0):
            pulley_data["rope_1_connection"] = {
                "x": part.pulley_rope_1_connect_pos_x,
                "y": part.pulley_rope_1_connect_pos_y
            }
        if (part.pulley_rope_2_connect_pos_x != 0 or part.pulley_rope_2_connect_pos_y != 0):
            pulley_data["rope_2_connection"] = {
                "x": part.pulley_rope_2_connect_pos_x,
                "y": part.pulley_rope_2_connect_pos_y
            }
        if part.unknown_36_pulley != -1:  # Default is -1
            pulley_data["unknown_36"] = part.unknown_36_pulley
        if part.unknown_38 != -1:  # Default is -1
            pulley_data["unknown_38"] = part.unknown_38
        if part.unknown_40 != 0:
            pulley_data["unknown_40"] = part.unknown_40
        if part.unknown_42 != 0:
            pulley_data["unknown_42"] = part.unknown_42
        if part.pulley_connected_1 != -1:
            pulley_data["connected_1"] = part.pulley_connected_1
        if part.pulley_connected_2 != -1:
            pulley_data["connected_2"] = part.pulley_connected_2
        if part.unknown_50 != -1:  # Default is -1
            pulley_data["unknown_50"] = part.unknown_50
        if part.unknown_52 != -1:  # Default is -1
            pulley_data["unknown_52"] = part.unknown_52
        if part.rope_index != -1:
            pulley_data["rope_index"] = part.rope_index
        if pulley_data:  # Only add if there's data
            result["pulley_data"] = pulley_data
    elif isinstance(part, ProgrammableBall):
        result["programmable_ball_data"] = {
            "density": part.density,
            "elasticity": part.elasticity,
            "friction": part.friction,
            "gravity_buoyancy": part.gravity_buoyancy,
            "mass": part.mass,
            "appearance_2": part.appearance_2
        }
    
    return result

def dict_to_part(part_dict: dict) -> Part:
    """Convert a dictionary to a Part object"""
    # Get part type
    part_type = PartType[part_dict["part_type"]]
    
    # Convert flags
    flags_1 = list_to_flags1(part_dict.get("flags_1", []))
    flags_2 = list_to_flags2(part_dict.get("flags_2", []))
    flags_3 = list_to_flags3(part_dict.get("flags_3", []))
    
    # Basic fields
    pos = part_dict.get("position", {"x": 0, "y": 0})
    
    # Get size from JSON or use defaults for this part type
    if "size" in part_dict:
        size = part_dict["size"]
        width_1 = size["width_1"]
        height_1 = size["height_1"]
        width_2 = size["width_2"]
        height_2 = size["height_2"]
    else:
        width_1, height_1, width_2, height_2 = get_default_part_size(part_type)
    
    # Create base kwargs
    kwargs = {
        "part_type": part_type,
        "flags_1": flags_1,
        "flags_2": flags_2,
        "flags_3": flags_3,
        "pos_x": pos["x"],
        "pos_y": pos["y"],
        "width_1": width_1,
        "height_1": height_1,
        "width_2": width_2,
        "height_2": height_2,
        "appearance": part_dict.get("appearance", 0),
        "behavior": part_dict.get("behavior", 0),
        "unknown_10": 0,  # Always 0, not in JSON
        "unknown_26": 0,  # Always 0, not in JSON
        "unknown_32": 0,  # Always 0, not in JSON
        "unknown_36": 0   # Always 0, not in JSON
    }
    
    # Belt connection
    if "belt_connection" in part_dict:
        bc = part_dict["belt_connection"]
        kwargs["belt_connect_pos_x"] = bc["x"]
        kwargs["belt_connect_pos_y"] = bc["y"]
        kwargs["belt_line_distance"] = bc["distance"]
    
    # Rope connections
    if "rope_1_connection" in part_dict:
        rc = part_dict["rope_1_connection"]
        kwargs["rope_1_connect_pos_x"] = rc["x"]
        kwargs["rope_1_connect_pos_y"] = rc["y"]
    if "rope_2_connection" in part_dict:
        rc = part_dict["rope_2_connection"]
        kwargs["rope_2_connect_pos_x"] = rc["x"]
        kwargs["rope_2_connect_pos_y"] = rc["y"]
    
    # Connected parts
    kwargs["connected_1"] = part_dict.get("connected_1", -1)
    kwargs["connected_2"] = part_dict.get("connected_2", -1)
    kwargs["outlet_plugged_1"] = part_dict.get("outlet_plugged_1", -1)
    kwargs["outlet_plugged_2"] = part_dict.get("outlet_plugged_2", -1)
    
    # Create appropriate part type
    if "belt_data" in part_dict:
        bd = part_dict["belt_data"]
        kwargs.update({
            "unknown_28": bd.get("unknown_28", 0),
            "unknown_30": bd.get("unknown_30", 0),
            "belt_connected_part_1": bd.get("connected_part_1", -1),
            "belt_connected_part_2": bd.get("connected_part_2", -1),
            "unknown_36_belt": bd.get("unknown_36", 0),
            "unknown_38": bd.get("unknown_38", 0),
            "unknown_40": bd.get("unknown_40", 0),
            "unknown_42": bd.get("unknown_42", 0)
        })
        return Belt(**kwargs)
    elif "rope_data" in part_dict:
        rd = part_dict["rope_data"]
        kwargs.update({
            "rope_segment_length": rd.get("segment_length", 0),
            "unknown_28": rd.get("unknown_28", 0),
            "unknown_30": rd.get("unknown_30", 0),
            "unknown_32_rope": rd.get("unknown_32", 1),
            "rope_connected_part_1": rd.get("connected_part_1", -1),
            "rope_connected_part_2": rd.get("connected_part_2", -1),
            "part_1_connect_field_usage": rd.get("part_1_connect_field_usage", 0),
            "part_2_connect_field_usage": rd.get("part_2_connect_field_usage", 0),
            "unknown_44": rd.get("unknown_44", 0),
            "unknown_46": rd.get("unknown_46", 0)
        })
        return Rope(**kwargs)
    elif "pulley_data" in part_dict:
        pd = part_dict["pulley_data"]
        kwargs.update({
            "unknown_28": pd.get("unknown_28", 0),
            "unknown_30": pd.get("unknown_30", 0),
            "unknown_32_pulley": pd.get("unknown_32", 1),
            "pulley_rope_1_connect_pos_x": pd["rope_1_connection"]["x"],
            "pulley_rope_1_connect_pos_y": pd["rope_1_connection"]["y"],
            "pulley_rope_2_connect_pos_x": pd["rope_2_connection"]["x"],
            "pulley_rope_2_connect_pos_y": pd["rope_2_connection"]["y"],
            "unknown_36_pulley": pd.get("unknown_36", -1),
            "unknown_38": pd.get("unknown_38", -1),
            "unknown_40": pd.get("unknown_40", 0),
            "unknown_42": pd.get("unknown_42", 0),
            "pulley_connected_1": pd.get("connected_1", -1),
            "pulley_connected_2": pd.get("connected_2", -1),
            "unknown_50": pd.get("unknown_50", -1),
            "unknown_52": pd.get("unknown_52", -1),
            "rope_index": pd.get("rope_index", -1)
        })
        return Pulley(**kwargs)
    elif "programmable_ball_data" in part_dict:
        pbd = part_dict["programmable_ball_data"]
        kwargs.update({
            "density": pbd.get("density", 2832),
            "elasticity": pbd.get("elasticity", 128),
            "friction": pbd.get("friction", 16),
            "gravity_buoyancy": pbd.get("gravity_buoyancy", 269),
            "mass": pbd.get("mass", 200),
            "appearance_2": pbd.get("appearance_2", 0)
        })
        return ProgrammableBall(**kwargs)
    else:
        return Part(**kwargs)

def tim_to_json(tim_filepath: str) -> dict:
    """Parse a TIM file and convert to JSON-serializable dictionary"""
    with open(tim_filepath, 'rb') as f:
        data = f.read()
    
    offset = 0
    
    # Magic number
    _magic = struct.unpack_from('>I', data, offset)[0]
    offset += 4
    
    # Background
    bg_unknown, bg_color = struct.unpack_from('>BB', data, offset)
    offset += 2
    
    # Quiz title (null-terminated string)
    title_start = offset
    while data[offset] != 0:
        offset += 1
    offset += 1
    quiz_title = data[title_start:offset-1].decode('latin-1')
    
    # Goal description (null-terminated string)
    desc_start = offset
    while data[offset] != 0:
        offset += 1
    offset += 1
    goal_description = data[desc_start:offset-1].decode('latin-1')
    
    # Hints
    num_hints = struct.unpack_from('<H', data, offset)[0]
    offset += 2
    offset += 7 * 8  # Skip hint data
    
    # Global puzzle information
    pressure, gravity, unk4, unk6, music, num_fixed, num_moving, unk14 = struct.unpack_from('<hhHHHHHH', data, offset)
    offset += 16
    
    # Parse normal parts
    normal_parts = []
    for _ in range(num_moving):
        part = Part.from_bytes(data, offset)
        offset += 48
        normal_parts.append(part_to_dict(part))
    
    # Solution information
    _num_conditions = struct.unpack_from('<H', data, offset)[0]
    offset += 2
    
    solution_conditions = []
    for _ in range(8):
        cond_data = struct.unpack_from('<hHHHhhhh', data, offset)
        offset += 16
        part_idx, state1, state2, count, rect_x, rect_y, rect_w, rect_h = cond_data
        if part_idx != -1 or state1 != 0 or state2 != 0 or count != 0:
            solution_conditions.append({
                "part_index": part_idx,
                "state_1": state1,
                "state_2": state2,
                "count": count,
                "rectangle": {
                    "x": rect_x,
                    "y": rect_y,
                    "width": rect_w,
                    "height": rect_h
                }
            })
    
    delay = struct.unpack_from('<H', data, offset)[0]
    
    # Build JSON structure
    result: dict[str,object] = {
        "version": "TIM2",
        "title": quiz_title,
        "description": goal_description
    }
    
    # Only include background.unknown if it's not 0
    bg_data = {"color": bg_color}
    if bg_unknown != 0:
        bg_data["unknown"] = bg_unknown
    result["background"] = bg_data
    
    # Build global_settings, excluding zero unknowns
    global_settings = {
        "pressure": pressure,
        "gravity": gravity,
        "music": music
    }
    if unk4 != 0:
        global_settings["unknown_4"] = unk4
    if unk6 != 0:
        global_settings["unknown_6"] = unk6
    if unk14 != 0:
        global_settings["unknown_14"] = unk14
    result["global_settings"] = global_settings
    
    # Only include hints if there are any
    if num_hints > 0:
        result["hints"] = {"count": num_hints}
    
    result["parts"] = normal_parts
    
    # Solution
    solution_data = {}
    if solution_conditions:
        solution_data["conditions"] = solution_conditions
    if delay != 0:
        solution_data["delay"] = delay
    if solution_data:
        result["solution"] = solution_data
    
    return result

def json_to_tim(json_data: dict) -> bytes:
    """Convert a JSON dictionary to TIM file bytes"""
    # Extract data
    title = json_data["title"].encode('latin-1') + b'\0'
    description = json_data["description"].encode('latin-1') + b'\0'
    bg = json_data["background"]
    settings = json_data["global_settings"]
    parts_data = json_data["parts"]
    solution = json_data.get("solution", {})
    
    # Convert parts
    parts = [dict_to_part(p) for p in parts_data]
    
    # Count part types
    num_normal = len([p for p in parts if isinstance(p, Part) and not isinstance(p, (Belt, Rope, Pulley, ProgrammableBall))])
    num_belts = len([p for p in parts if isinstance(p, Belt)])
    num_ropes = len([p for p in parts if isinstance(p, Rope)])
    num_pulleys = len([p for p in parts if isinstance(p, Pulley)])
    num_programmable = len([p for p in parts if isinstance(p, ProgrammableBall)])
    
    # Calculate file size
    filesize = calculate_filesize(len(title), len(description), num_normal, num_belts, num_ropes, num_pulleys, num_programmable)
    buffer = bytearray(filesize)
    offset = 0
    
    # Magic number
    struct.pack_into('>I', buffer, offset, 0xEFAC1301)
    offset += 4
    
    # Background (unknown defaults to 0 if not present)
    struct.pack_into('>BB', buffer, offset, bg.get("unknown", 0), bg["color"])
    offset += 2
    
    # Title and description
    struct.pack_into(f'<{len(title)}s', buffer, offset, title)
    offset += len(title)
    struct.pack_into(f'<{len(description)}s', buffer, offset, description)
    offset += len(description)
    
    # Hints (empty for now)
    hints_count = json_data.get("hints", {}).get("count", 0)
    struct.pack_into('<H', buffer, offset, hints_count)
    offset += 2
    offset += 7 * 8  # Skip hint data
    
    # Global settings
    num_fixed = num_belts + num_ropes + num_pulleys
    num_moving = len(parts) - num_fixed
    struct.pack_into('<hhHHHHHH', buffer, offset,
                     settings["pressure"], settings["gravity"],
                     settings.get("unknown_4", 0), settings.get("unknown_6", 0),
                     settings["music"], num_fixed, num_moving,
                     settings.get("unknown_14", 0))
    offset += 16
    
    # Write parts
    for part in parts:
        part_bytes = part.to_bytes()
        buffer[offset:offset+len(part_bytes)] = part_bytes
        offset += len(part_bytes)
    
    # Solution information
    conditions = solution.get("conditions", [])
    struct.pack_into('<H', buffer, offset, len(conditions))
    offset += 2
    
    # Write up to 8 conditions
    for i in range(8):
        if i < len(conditions):
            cond = conditions[i]
            rect = cond["rectangle"]
            struct.pack_into('<hHHHhhhh', buffer, offset,
                           cond["part_index"], cond["state_1"], cond["state_2"],
                           cond["count"], rect["x"], rect["y"],
                           rect["width"], rect["height"])
        else:
            struct.pack_into('<hHHHhhhh', buffer, offset, -1, 0, 0, 0, 0, 0, 0, 0)
        offset += 16
    
    struct.pack_into('<H', buffer, offset, solution.get("delay", 0))
    offset += 2
    
    return bytes(buffer)

def parse_tim_file(filepath: str):
    '''Parse a TIM file and print all information to console'''
    with open(filepath, 'rb') as f:
        data = f.read()
    
    offset = 0
    
    # Magic number
    magic = struct.unpack_from('>I', data, offset)[0]
    offset += 4
    print(f"Magic Number: 0x{magic:08X}")
    if magic != 0xEFAC1301:
        print("Warning: Invalid magic number!")
    
    # Background
    bg_unknown, bg_color = struct.unpack_from('>BB', data, offset)
    offset += 2
    print(f"Background: unknown={bg_unknown}, color={bg_color}")
    
    # Quiz title (null-terminated string)
    title_start = offset
    while data[offset] != 0:
        offset += 1
    offset += 1  # Include null terminator
    quiz_title = data[title_start:offset-1].decode('latin-1')
    print(f"Quiz Title: '{quiz_title}'")
    
    # Goal description (null-terminated string)
    desc_start = offset
    while data[offset] != 0:
        offset += 1
    offset += 1  # Include null terminator
    goal_description = data[desc_start:offset-1].decode('latin-1')
    print(f"Goal Description: '{goal_description}'")
    
    # Hints (2 byte num + 8 * 7 bytes)
    num_hints = struct.unpack_from('<H', data, offset)[0]
    offset += 2
    print(f"Number of Hints: {num_hints}")
    # Skip hint data (8 hints * 7 bytes each)
    offset += 7 * 8
    
    # Global puzzle information
    pressure, gravity, unk4, unk6, music, num_fixed, num_moving, unk14 = struct.unpack_from('<hhHHHHHH', data, offset)
    offset += 16
    print(f"\n{'='*60}")
    print("Global Puzzle Information:")
    print(f"{'='*60}")
    print(f"  Pressure: {pressure}")
    print(f"  Gravity: {gravity}")
    print(f"  Unknown_4: {unk4}")
    print(f"  Unknown_6: {unk6}")
    print(f"  Music: {music}")
    print(f"  Fixed Parts: {num_fixed}")
    print(f"  Moving Parts: {num_moving}")
    print(f"  Unknown_14: {unk14}")
    
    def get_part_type_name(part_type_val: int) -> str:
        """Get human-readable part type name"""
        try:
            return PartType(part_type_val).name
        except ValueError:
            return f"UNKNOWN_{part_type_val}"
    
    def format_flags1(flags: int) -> list[str]:
        """Format Flags1 into readable list"""
        result = []
        if flags & Flags1.UNKNOWN_0x40:
            result.append("UNKNOWN_0x40")
        if flags & Flags1.CAN_FLIP_VERTICAL:
            result.append("CAN_FLIP_VERTICAL")
        if flags & Flags1.CAN_FLIP_HORIZONTAL:
            result.append("CAN_FLIP_HORIZONTAL")
        if flags & Flags1.MOVING_PART:
            result.append("MOVING_PART")
        if flags & Flags1.FIXED_PART_1:
            result.append("FIXED_PART_1")
        if flags & Flags1.FIXED_PART_2:
            result.append("FIXED_PART_2")
        return result if result else ["NONE"]
    
    def format_flags2(flags: int) -> list[str]:
        """Format Flags2 into readable list"""
        result = []
        if flags & Flags2.BELT_CAN_CONNECT:
            result.append("BELT_CAN_CONNECT")
        if flags & Flags2.BELT_IS_CONNECTED:
            result.append("BELT_IS_CONNECTED")
        if flags & Flags2.ROPE_CAN_CONNECT:
            result.append("ROPE_CAN_CONNECT")
        if flags & Flags2.ROPE_CAN_CONNECT_2:
            result.append("ROPE_CAN_CONNECT_2")
        if flags & Flags2.SPRITE_FLIP_HORIZONTAL:
            result.append("SPRITE_FLIP_HORIZONTAL")
        if flags & Flags2.SPRITE_FLIP_VERTICAL:
            result.append("SPRITE_FLIP_VERTICAL")
        if flags & Flags2.PROBABLY_UNUSED:
            result.append("PROBABLY_UNUSED")
        if flags & Flags2.CAN_STRETCH_ONE_DIR:
            result.append("CAN_STRETCH_ONE_DIR")
        if flags & Flags2.CAN_STRETCH_BOTH:
            result.append("CAN_STRETCH_BOTH")
        return result if result else ["NONE"]
    
    def format_flags3(flags: int) -> list[str]:
        """Format Flags3 into readable list"""
        result = []
        if flags & Flags3.CAN_PLUG_OUTLET:
            result.append("CAN_PLUG_OUTLET")
        if flags & Flags3.IS_ELECTRIC_OUTLET:
            result.append("IS_ELECTRIC_OUTLET")
        if flags & Flags3.CAN_BURN_OR_FUSE:
            result.append("CAN_BURN_OR_FUSE")
        if flags & Flags3.UNKNOWN_0x8:
            result.append("UNKNOWN_0x8")
        if flags & Flags3.LOCKED:
            result.append("LOCKED")
        if flags & Flags3.SIZABLE_SCENERY:
            result.append("SIZABLE_SCENERY")
        if flags & Flags3.UNKNOWN_0x100:
            result.append("UNKNOWN_0x100")
        if flags & Flags3.SHOW_PROGRAM_ICON:
            result.append("SHOW_PROGRAM_ICON")
        if flags & Flags3.SCENERY_PART:
            result.append("SCENERY_PART")
        if flags & Flags3.WALL_PART:
            result.append("WALL_PART")
        if flags & Flags3.SHOW_SOLUTION_ICON:
            result.append("SHOW_SOLUTION_ICON")
        return result if result else ["NONE"]
    
    # Parse normal parts
    print(f"\n{'='*60}")
    print(f"Normal Parts ({num_moving}):")
    print(f"{'='*60}")
    for i in range(num_moving):
        part = Part.from_bytes(data, offset)
        offset += 48
        
        print(f"\n  Part {i}: {get_part_type_name(part.part_type)}")
        print(f"    Position: ({part.pos_x}, {part.pos_y})")
        print(f"    Size 1: {part.width_1} x {part.height_1}")
        print(f"    Size 2: {part.width_2} x {part.height_2}")
        print(f"    Appearance: {part.appearance}")
        print(f"    Behavior: {part.behavior}")
        print(f"    Flags1 (0x{part.flags_1:04X}): {', '.join(format_flags1(part.flags_1))}")
        print(f"    Flags2 (0x{part.flags_2:04X}): {', '.join(format_flags2(part.flags_2))}")
        print(f"    Flags3 (0x{part.flags_3:04X}): {', '.join(format_flags3(part.flags_3))}")
        
        if part.belt_connect_pos_x != 0 or part.belt_connect_pos_y != 0:
            print(f"    Belt Connect: ({part.belt_connect_pos_x}, {part.belt_connect_pos_y}), Distance: {part.belt_line_distance}")
        if part.rope_1_connect_pos_x != 0 or part.rope_1_connect_pos_y != 0:
            print(f"    Rope 1 Connect: ({part.rope_1_connect_pos_x}, {part.rope_1_connect_pos_y})")
        if part.rope_2_connect_pos_x != 0 or part.rope_2_connect_pos_y != 0:
            print(f"    Rope 2 Connect: ({part.rope_2_connect_pos_x}, {part.rope_2_connect_pos_y})")
        if part.connected_1 != -1:
            print(f"    Connected 1: {part.connected_1}")
        if part.connected_2 != -1:
            print(f"    Connected 2: {part.connected_2}")
        if part.outlet_plugged_1 != -1:
            print(f"    Outlet Plugged 1: {part.outlet_plugged_1}")
        if part.outlet_plugged_2 != -1:
            print(f"    Outlet Plugged 2: {part.outlet_plugged_2}")
        if part.unknown_10 != 0:
            print(f"    Unknown_10: {part.unknown_10}")
        if part.unknown_26 != 0:
            print(f"    Unknown_26: {part.unknown_26}")
        if part.unknown_32 != 0:
            print(f"    Unknown_32: {part.unknown_32}")
        if part.unknown_36 != 0:
            print(f"    Unknown_36: {part.unknown_36}")
    
    # Parse belts
    if num_fixed > 0:
        print(f"\n{'='*60}")
        print("Belts:")
        print(f"{'='*60}")
        # Belts would be 52 bytes each - need to determine how many
        # For now, we'll try to detect them based on part type
    
    # Parse ropes
    print(f"\n{'='*60}")
    print("Ropes:")
    print(f"{'='*60}")
    print("  (Not yet in generated files)")
    
    # Parse pulleys
    print(f"\n{'='*60}")
    print("Pulleys:")
    print(f"{'='*60}")
    print("  (Not yet in generated files)")
    
    # Solution information (132 bytes)
    print(f"\n{'='*60}")
    print("Solution Information:")
    print(f"{'='*60}")
    num_conditions = struct.unpack_from('<H', data, offset)[0]
    offset += 2
    print(f"Number of Conditions: {num_conditions}")
    for i in range(8):
        cond_data = struct.unpack_from('<hHHHhhhh', data, offset)
        offset += 16
        part_idx, state1, state2, count, rect_x, rect_y, rect_w, rect_h = cond_data
        if part_idx != -1 or state1 != 0 or state2 != 0 or count != 0:
            print(f"\n  Condition {i}:")
            print(f"    Part Index: {part_idx}")
            print(f"    State 1: {state1}")
            print(f"    State 2: {state2}")
            print(f"    Count: {count}")
            print(f"    Rectangle: ({rect_x}, {rect_y}) {rect_w}x{rect_h}")
    
    delay = struct.unpack_from('<H', data, offset)[0]
    offset += 2
    print(f"\nDelay: {delay}")
    
    print(f"\n{'='*60}")
    print("File Statistics:")
    print(f"{'='*60}")
    print(f"Total file size: {len(data)} bytes")
    print(f"Bytes parsed: {offset}")
    if offset != len(data):
        print(f"Warning: {len(data) - offset} bytes remaining!")
    else:
        print("File parsed successfully!")


def main():
    parser = argparse.ArgumentParser(description='Generate TIM2 level files')
    parser.add_argument('--title', type=str, default='My spiral test', 
                        help='Quiz title for the level')
    parser.add_argument('--description', type=str, default='Press start and it will lag like hell!',
                        help='Goal description for the level')
    parser.add_argument('--output', type=str, default='SPIRAL.TIM',
                        help='Output file path (relative or absolute)')
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug output (print buffer hex)')
    parser.add_argument('--color', type=int, default=3,
                        help='Background color from 0 to 16')
    parser.add_argument('--music', type=int, default=1000,
                        help='Music from 1000 to 1023')
    parser.add_argument('--parse', type=str, metavar='FILE',
                        help='Parse and display information from a TIM file')
    parser.add_argument('--tim2json', type=str, metavar='FILE',
                        help='Convert a TIM file to JSON format')
    parser.add_argument('--json2tim', type=str, metavar='FILE',
                        help='Convert a JSON file to TIM format')
    
    args = parser.parse_args()
    
    # If tim2json mode, convert TIM to JSON and exit
    if args.tim2json:
        input_path = Path(args.tim2json)
        output_path = input_path.with_suffix('.json')
        
        print(f"Converting {input_path} to JSON...")
        json_data = tim_to_json(str(input_path))
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        print(f"Saved to {output_path}")
        return
    
    # If json2tim mode, convert JSON to TIM and exit
    if args.json2tim:
        input_path = Path(args.json2tim)
        output_path = input_path.with_suffix('.TIM')
        
        print(f"Converting {input_path} to TIM...")
        
        with open(input_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        tim_bytes = json_to_tim(json_data)
        
        with open(output_path, 'wb') as f:
            f.write(tim_bytes)
        
        print(f"Saved {len(tim_bytes)} bytes to {output_path}")
        return
    
    # If parse mode, parse the file and exit
    if args.parse:
        parse_tim_file(args.parse)
        return
    
    # Ensure strings are null-terminated and encoded as bytes
    quiz_title = args.title.encode('latin-1') + b'\0'
    goal_description = args.description.encode('latin-1') + b'\0'
    
    color = args.color
    music = args.music

    num_basketballs = 150

    buffer = make_buffer(
        color=color,
        music=music,
        quiz_title=quiz_title,
        goal_description=goal_description,
        normal_parts=[i for i in range(num_basketballs)],
        belts=[],
        ropes=[],
        pulleys=[],
    )

    if args.debug:
        print(buffer.hex(' ', bytes_per_sep=2))

    filename = args.output
    with open(filename, 'wb') as file:
        file.write(buffer)
        print(f'Saved {len(buffer)} bytes into {filename}')

    #Readback to be sure
    with open(filename, 'rb') as file:
        file_content = file.read()
        assert len(file_content) == len(buffer)
        assert file_content == buffer


if __name__ == "__main__":
    main()
