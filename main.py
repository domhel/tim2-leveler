import struct
import math
import argparse
from enum import IntEnum, IntFlag
from dataclasses import dataclass, field
from typing import Optional


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
    print(f"Background Color: {bg_color}")
    
    # Quiz title (null-terminated string)
    title_start = offset
    while data[offset] != 0:
        offset += 1
    offset += 1  # Include null terminator
    quiz_title = data[title_start:offset-1].decode('latin-1')
    print(f"Quiz Title: {quiz_title}")
    
    # Goal description (null-terminated string)
    desc_start = offset
    while data[offset] != 0:
        offset += 1
    offset += 1  # Include null terminator
    goal_description = data[desc_start:offset-1].decode('latin-1')
    print(f"Goal Description: {goal_description}")
    
    # Hints (2 byte num + 8 * 7 bytes)
    num_hints = struct.unpack_from('<H', data, offset)[0]
    offset += 2
    print(f"Number of Hints: {num_hints}")
    # Skip hint data (8 hints * 7 bytes each)
    offset += 7 * 8
    
    # Global puzzle information
    pressure, gravity, unk4, unk6, music, num_fixed, num_moving, unk14 = struct.unpack_from('<hhHHHHHH', data, offset)
    offset += 16
    print(f"\nGlobal Puzzle Information:")
    print(f"  Pressure: {pressure}")
    print(f"  Gravity: {gravity}")
    print(f"  Music: {music}")
    print(f"  Fixed Parts: {num_fixed}")
    print(f"  Moving Parts: {num_moving}")
    
    # Parse normal parts
    print(f"\nNormal Parts ({num_moving}):")
    for i in range(num_moving):
        part_data = struct.unpack_from('<HHHHHHHHHHhhHHBBHHBBHBBhhhh', data, offset)
        offset += 48
        part_type, flags1, flags2, flags3, appearance, unk10, w1, h1, w2, h2, x, y, behavior, unk26, \
        belt_x, belt_y, belt_dist, unk32, rope1_x, rope1_y, unk36, rope2_x, rope2_y, \
        conn1, conn2, outlet1, outlet2 = part_data
        print(f"  Part {i}: Type={part_type}, Pos=({x},{y}), Size=({w1}x{h1})")
        print(f"    Flags1=0x{flags1:04X}, Flags2=0x{flags2:04X}, Flags3=0x{flags3:04X}")
        print(f"    Appearance={appearance}, Behavior={behavior}")
    
    # Parse belts
    print(f"\nBelts ({num_fixed if num_fixed > 0 else 0}):")
    # Belts would be 52 bytes each, but we don't have any in current implementation
    
    # Parse ropes
    print(f"\nRopes:")
    # Ropes would be 54 bytes each
    
    # Parse pulleys
    print(f"\nPulleys:")
    # Pulleys would be 56 bytes each
    
    # Solution information (132 bytes)
    num_conditions = struct.unpack_from('<H', data, offset)[0]
    offset += 2
    print(f"\nSolution Conditions: {num_conditions}")
    for i in range(8):
        cond_data = struct.unpack_from('<hHHHhhhh', data, offset)
        offset += 16
        part_idx, state1, state2, count, rect_x, rect_y, rect_w, rect_h = cond_data
        if part_idx != -1 or state1 != 0 or state2 != 0:
            print(f"  Condition {i}: Part={part_idx}, State1={state1}, State2={state2}, Count={count}, Rect=({rect_x},{rect_y},{rect_w},{rect_h})")
    
    delay = struct.unpack_from('<H', data, offset)[0]
    offset += 2
    print(f"Delay: {delay}")
    
    print(f"\nTotal file size: {len(data)} bytes")
    print(f"Bytes parsed: {offset}")
    if offset != len(data):
        print(f"Warning: {len(data) - offset} bytes remaining!")


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
    
    args = parser.parse_args()
    
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
