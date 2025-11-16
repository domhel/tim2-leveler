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
    UNKNOWN_19 = 19
    UNKNOWN_20 = 20
    UNKNOWN_21 = 21
    UNKNOWN_22 = 22
    UNKNOWN_23 = 23
    UNKNOWN_24 = 24
    UNKNOWN_25 = 25
    UNKNOWN_26 = 26
    UNKNOWN_27 = 27
    UNKNOWN_28 = 28
    UNKNOWN_29 = 29
    UNKNOWN_30 = 30
    UNKNOWN_31 = 31
    UNKNOWN_32 = 32
    UNKNOWN_33 = 33
    UNKNOWN_34 = 34
    UNKNOWN_35 = 35
    UNKNOWN_36 = 36
    UNKNOWN_37 = 37
    UNKNOWN_38 = 38
    UNKNOWN_39 = 39
    UNKNOWN_40 = 40
    UNKNOWN_41 = 41
    UNKNOWN_42 = 42
    UNKNOWN_43 = 43
    UNKNOWN_44 = 44
    UNKNOWN_45 = 45
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
    UNKNOWN_65 = 65
    UNKNOWN_66 = 66
    UNKNOWN_67 = 67
    UNKNOWN_68 = 68
    UNKNOWN_69 = 69
    UNKNOWN_70 = 70
    UNKNOWN_71 = 71
    UNKNOWN_72 = 72
    UNKNOWN_73 = 73
    UNKNOWN_74 = 74
    UNKNOWN_75 = 75
    STEEL_CABLE = 76
    UNKNOWN_77 = 77
    UNKNOWN_78 = 78
    UNKNOWN_79 = 79
    UNKNOWN_80 = 80
    UNKNOWN_81 = 81
    UNKNOWN_82 = 82
    UNKNOWN_83 = 83
    UNKNOWN_84 = 84
    UNKNOWN_85 = 85
    UNKNOWN_86 = 86
    PROGRAMMABLE_BALL = 87
    UNKNOWN_88 = 88
    UNKNOWN_89 = 89
    UNKNOWN_90 = 90
    UNKNOWN_91 = 91
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
    UNKNOWN_110 = 110
    UNKNOWN_111 = 111
    UNKNOWN_112 = 112
    UNKNOWN_113 = 113
    UNKNOWN_114 = 114
    UNKNOWN_115 = 115
    UNKNOWN_116 = 116
    UNKNOWN_117 = 117
    UNKNOWN_118 = 118
    UNKNOWN_119 = 119
    UNKNOWN_120 = 120
    UNKNOWN_121 = 121
    UNKNOWN_122 = 122
    UNKNOWN_123 = 123
    UNKNOWN_124 = 124
    UNKNOWN_125 = 125
    UNKNOWN_126 = 126
    UNKNOWN_127 = 127
    UNKNOWN_128 = 128
    UNKNOWN_129 = 129
    UNKNOWN_130 = 130
    UNKNOWN_131 = 131
    UNKNOWN_132 = 132
    UNKNOWN_133 = 133
    UNKNOWN_134 = 134
    UNKNOWN_135 = 135
    UNKNOWN_136 = 136
    UNKNOWN_137 = 137
    UNKNOWN_138 = 138
    UNKNOWN_139 = 139
    UNKNOWN_140 = 140
    UNKNOWN_141 = 141
    UNKNOWN_142 = 142
    UNKNOWN_143 = 143
    UNKNOWN_144 = 144
    UNKNOWN_145 = 145
    UNKNOWN_146 = 146
    UNKNOWN_147 = 147
    UNKNOWN_148 = 148
    UNKNOWN_149 = 149
    UNKNOWN_150 = 150
    EMPTY_SLOT = 65535  # 0xFFFF - likely an empty or placeholder slot
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


def get_default_part_flags(part_type: PartType) -> tuple[int, int, int]:
    """Get default flags for a part type (flags_1, flags_2, flags_3)"""
    # Default flags extracted from ALL_ITEMS.TIM
    flags_map = {
        0: (0x1000, 0x0000, 0x8008),  # BOWLING_BALL
        1: (0x6000, 0x0180, 0x2000),  # RED_BRICK_WALL
        2: (0x6600, 0x0080, 0x0000),  # WOOD_INCLINE
        3: (0x6400, 0x000c, 0x0000),  # TIPSY_TRAILER
        4: (0x1000, 0x0004, 0x8408),  # BALLOON
        5: (0x6000, 0x0081, 0x0000),  # CONVEYOR_BELT
        6: (0x6400, 0x0001, 0x8000),  # MOUSE_MOTOR
        7: (0x6000, 0x0004, 0x0008),  # PULLEY
        9: (0x1000, 0x0000, 0x8008),  # BASKETBALL
        11: (0x1000, 0x0004, 0x8008),  # LAUNDRY_BASKET
        12: (0x1400, 0x0000, 0x8008),  # CURIE_CAT
        13: (0x6400, 0x0001, 0x8000),  # JACK_IN_THE_BOX
        14: (0x6000, 0x0001, 0x0000),  # GEAR
        15: (0x6000, 0x0000, 0x8008),  # FISH_TANK
        16: (0x6400, 0x0000, 0x8008),  # BIKE_PUMP
        17: (0x1000, 0x0004, 0x8008),  # BUCKET
        18: (0x6600, 0x0000, 0x800c),  # CANNON
        19: (0x1400, 0x0000, 0x800c),  # UNKNOWN_19
        21: (0x6200, 0x0000, 0x0002),  # UNKNOWN_21
        22: (0x6000, 0x0004, 0x8008),  # UNKNOWN_22
        23: (0x6200, 0x0004, 0x0008),  # UNKNOWN_23
        24: (0x6400, 0x0000, 0x8009),  # UNKNOWN_24
        25: (0x6400, 0x0000, 0x8008),  # UNKNOWN_25
        26: (0x6000, 0x0001, 0x000a),  # UNKNOWN_26
        27: (0x6400, 0x0004, 0x8408),  # UNKNOWN_27
        28: (0x1000, 0x0000, 0x8008),  # UNKNOWN_28
        29: (0x6000, 0x0004, 0x8008),  # UNKNOWN_29
        30: (0x6400, 0x0000, 0x0008),  # UNKNOWN_30
        31: (0x6400, 0x0005, 0x8008),  # UNKNOWN_31
        35: (0x6400, 0x0000, 0x8008),  # UNKNOWN_35
        36: (0x1600, 0x0000, 0x800c),  # UNKNOWN_36
        37: (0x6400, 0x0000, 0x8008),  # UNKNOWN_37
        38: (0x6000, 0x0000, 0x000a),  # UNKNOWN_38
        39: (0x6000, 0x0000, 0x0008),  # UNKNOWN_39
        40: (0x6400, 0x0001, 0x8008),  # UNKNOWN_40
        42: (0x1400, 0x0000, 0x8008),  # UNKNOWN_42
        43: (0x1000, 0x0000, 0x8008),  # UNKNOWN_43
        44: (0x1000, 0x0000, 0x8008),  # UNKNOWN_44
        45: (0x1400, 0x0000, 0x800c),  # UNKNOWN_45
        46: (0x6000, 0x0180, 0x2000),  # PIPE_WALL
        47: (0x6600, 0x0000, 0x0000),  # CURVED_PIPE_WALL
        48: (0x6000, 0x0180, 0x2000),  # WOOD_WALL
        50: (0x6400, 0x0001, 0x8009),  # ELECTRIC_MOTOR
        51: (0x6400, 0x0000, 0x8009),  # VACUUM
        52: (0x1000, 0x0000, 0x8008),  # CHEESE
        53: (0x6600, 0x0000, 0x0008),  # THUMB_TACK
        54: (0x1400, 0x0000, 0x8408),  # MEL_SCHLEMMING
        55: (0x6000, 0x0000, 0x8008),  # REMOTE_CONTROL_EXPLOSIVES
        56: (0x6000, 0x0180, 0x2000),  # CAUTION_WALL
        57: (0x6600, 0x0000, 0x0000),  # LARGE_CURVED_PIPE
        58: (0x6000, 0x0000, 0x8408),  # MELS_HOUSE
        59: (0x1000, 0x0000, 0x8008),  # SUPER_BALL
        60: (0x6000, 0x0180, 0x2000),  # GRASS_FLOOR
        61: (0x6400, 0x0000, 0x8000),  # ALLIGATOR
        62: (0x1400, 0x0000, 0x8008),  # COFFEE_POT
        63: (0x1000, 0x0000, 0x8408),  # POOL_BALL
        64: (0x6000, 0x0000, 0x0008),  # PINBALL_BUMPER
        66: (0x6000, 0x0000, 0x8008),  # UNKNOWN_66
        67: (0x6000, 0x0000, 0x8009),  # UNKNOWN_67
        68: (0x1000, 0x0000, 0x8008),  # UNKNOWN_68
        69: (0x6000, 0x0000, 0x8000),  # UNKNOWN_69
        70: (0x1600, 0x0000, 0x800c),  # UNKNOWN_70
        71: (0x6000, 0x0000, 0x0400),  # UNKNOWN_71
        73: (0x6400, 0x0000, 0x8000),  # UNKNOWN_73
        74: (0x1000, 0x0000, 0x8008),  # UNKNOWN_74
        75: (0x6400, 0x0004, 0x8008),  # UNKNOWN_75
        77: (0x6400, 0x0000, 0x8008),  # UNKNOWN_77
        78: (0x6000, 0x0000, 0x8008),  # UNKNOWN_78
        79: (0x1000, 0x0004, 0x800c),  # UNKNOWN_79
        80: (0x1000, 0x0000, 0x840c),  # UNKNOWN_80
        81: (0x6400, 0x0000, 0x8409),  # UNKNOWN_81
        82: (0x6000, 0x0180, 0x2000),  # UNKNOWN_82
        83: (0x6000, 0x0180, 0x2000),  # UNKNOWN_83
        84: (0x6000, 0x0180, 0x2000),  # UNKNOWN_84
        85: (0x6000, 0x0180, 0x2000),  # UNKNOWN_85
        86: (0x6000, 0x0001, 0x0000),  # UNKNOWN_86
        87: (0x1000, 0x0000, 0x8408),  # PROGRAMMABLE_BALL
        88: (0x6600, 0x0000, 0x0000),  # UNKNOWN_88
        89: (0x6600, 0x0005, 0x0008),  # UNKNOWN_89
        90: (0x6200, 0x0005, 0x0008),  # UNKNOWN_90
        91: (0x6600, 0x0000, 0x8009),  # UNKNOWN_91
        92: (0x6600, 0x0000, 0x8009),  # GREEN_LASER
        93: (0x6600, 0x0000, 0x8009),  # BLUE_LASER
        94: (0x6600, 0x0000, 0x0008),  # ANGLED_MIRROR
        95: (0x6600, 0x0000, 0x0008),  # LASER_MIXER
        96: (0x6000, 0x0000, 0x040a),  # LASER_ACTIVATED_PLUG
        97: (0x6000, 0x0180, 0x0000),  # LARGE_PIPES
        98: (0x6000, 0x0000, 0x0000),  # T_CONNECTOR
        99: (0x6600, 0x0080, 0x0000),  # GRASS_INCLINE
        100: (0x6600, 0x0080, 0x0000),  # LOG_INCLINE
        101: (0x6600, 0x0080, 0x0000),  # GRANITE_INCLINE
        102: (0x6600, 0x0080, 0x0000),  # BRICK_INCLINE
        103: (0x6000, 0x0000, 0x0000),  # ARCHWAY
        104: (0x6000, 0x0000, 0x0000),  # WOODEN_BARRIER
        105: (0x6000, 0x0000, 0x0000),  # SCAFFOLD_BARRIER
        106: (0x6000, 0x0000, 0x0000),  # LATTICE_ARCHWAY
        107: (0x6000, 0x0000, 0x8009),  # ELECTRIC_MIXER
        108: (0x1000, 0x0004, 0x8408),  # LEAKY_BUCKET
        109: (0x1400, 0x0000, 0x8008),  # BLIMP
        116: (0x6400, 0x0000, 0x0008),  # UNKNOWN_116
        117: (0x6600, 0x0000, 0x8008),  # UNKNOWN_117
        118: (0x6200, 0x0180, 0x2000),  # UNKNOWN_118
        119: (0x6600, 0x0000, 0x8000),  # UNKNOWN_119
        120: (0x6000, 0x0000, 0x000a),  # UNKNOWN_120
        125: (0x6000, 0x0180, 0x2000),  # UNKNOWN_125
        126: (0x6600, 0x0080, 0x0000),  # UNKNOWN_126
        136: (0x6000, 0x0000, 0x8408),  # UNKNOWN_136
        137: (0x6400, 0x0000, 0x8408),  # UNKNOWN_137
        138: (0x1000, 0x0000, 0x800c),  # UNKNOWN_138
        139: (0x6400, 0x000c, 0x0000),  # UNKNOWN_139
        148: (0x6000, 0x0000, 0x8008),  # UNKNOWN_148
    }
    
    # Default flags for unknown parts: fixed, no special flags
    return flags_map.get(part_type, (0x6000, 0x0000, 0x0008))


def get_default_part_size(part_type: PartType) -> tuple[int, int, int, int]:
    """Get default size for a part type (width_1, height_1, width_2, height_2)"""
    # Default sizes extracted from ALL_ITEMS.TIM
    size_map = {
        0: (32, 32, 32, 32),
        1: (32, 16, 32, 16),
        2: (32, 32, 32, 32),
        3: (80, 39, 80, 39),
        4: (40, 51, 40, 51),
        5: (48, 16, 48, 16),
        6: (48, 32, 49, 33),
        7: (24, 22, 24, 22),
        9: (32, 32, 32, 32),
        11: (64, 62, 64, 62),
        12: (45, 42, 39, 42),
        13: (33, 32, 33, 32),
        14: (40, 35, 32, 32),
        15: (67, 51, 64, 51),
        16: (48, 51, 46, 51),
        17: (40, 49, 37, 49),
        18: (80, 61, 101, 78),
        19: (53, 15, 53, 15),
        21: (32, 32, 32, 32),
        22: (35, 37, 30, 37),
        23: (32, 15, 30, 15),
        24: (32, 46, 27, 46),
        25: (48, 21, 46, 21),
        26: (81, 34, 81, 34),
        27: (70, 44, 65, 44),
        28: (24, 18, 18, 18),
        29: (28, 65, 24, 65),
        30: (24, 40, 18, 40),
        31: (106, 79, 101, 79),
        35: (56, 39, 53, 39),
        36: (32, 85, 84, 84),
        37: (61, 36, 55, 36),
        38: (72, 32, 71, 32),
        39: (56, 27, 49, 27),
        40: (56, 55, 50, 55),
        42: (24, 20, 20, 20),
        43: (24, 23, 23, 23),
        44: (16, 15, 15, 15),
        45: (56, 29, 51, 29),
        46: (32, 16, 32, 16),
        47: (32, 32, 32, 32),
        48: (32, 16, 32, 16),
        50: (70, 54, 66, 54),
        51: (65, 33, 59, 33),
        52: (32, 18, 31, 18),
        53: (24, 24, 24, 24),
        54: (24, 26, 20, 26),
        55: (62, 48, 60, 48),
        56: (32, 16, 32, 16),
        57: (72, 64, 72, 64),
        58: (48, 64, 48, 64),
        59: (24, 23, 23, 23),
        60: (32, 16, 32, 16),
        61: (100, 16, 94, 16),
        62: (40, 41, 38, 41),
        63: (24, 23, 23, 23),
        64: (48, 41, 41, 41),
        66: (24, 21, 19, 21),
        67: (43, 51, 37, 51),
        68: (32, 32, 32, 32),
        69: (48, 16, 48, 16),
        70: (32, 95, 96, 96),
        71: (50, 32, 50, 32),
        73: (53, 49, 48, 49),
        74: (16, 29, 10, 29),
        75: (43, 23, 36, 23),
        77: (61, 33, 56, 33),
        78: (48, 34, 46, 34),
        79: (40, 83, 34, 83),
        80: (26, 86, 23, 86),
        81: (48, 35, 44, 35),
        82: (32, 16, 32, 16),
        83: (32, 16, 32, 16),
        84: (32, 16, 32, 16),
        85: (32, 16, 32, 16),
        86: (24, 17, 16, 16),
        87: (32, 27, 27, 27),
        88: (40, 48, 40, 48),
        89: (88, 49, 83, 49),
        90: (24, 69, 22, 69),
        91: (48, 18, 51, 51),
        92: (48, 18, 51, 51),
        93: (48, 18, 51, 51),
        94: (24, 23, 23, 23),
        95: (40, 40, 40, 40),
        96: (32, 32, 32, 32),
        97: (48, 38, 48, 38),
        98: (80, 80, 80, 80),
        99: (32, 32, 32, 32),
        100: (32, 32, 32, 32),
        101: (32, 32, 32, 32),
        102: (32, 32, 32, 32),
        103: (64, 64, 64, 64),
        104: (64, 64, 64, 64),
        105: (64, 64, 64, 64),
        106: (64, 64, 64, 64),
        107: (56, 55, 49, 55),
        108: (40, 50, 35, 50),
        109: (56, 36, 53, 36),
        116: (48, 41, 45, 41),
        117: (48, 9, 78, 78),
        118: (32, 32, 32, 32),
        119: (64, 64, 64, 64),
        120: (32, 32, 25, 32),
        125: (32, 16, 32, 16),
        126: (32, 32, 32, 32),
        136: (48, 43, 46, 43),
        137: (50, 40, 49, 40),
        138: (24, 33, 24, 33),
        139: (88, 40, 81, 40),
        148: (40, 32, 37, 32),
    }
    
    return size_map.get(part_type, (0x20, 0x20, 0x20, 0x20))


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


def parse_part_from_bytes(data: bytes, offset: int) -> tuple[Part, int]:
    """
    Parse a part from bytes, automatically detecting the part type and size.
    Returns (part, bytes_consumed).
    """
    # Peek at the part type
    part_type_value = struct.unpack_from('<H', data, offset)[0]
    
    # Determine the size based on part type
    if part_type_value == PartType.BELT:
        # Parse as Belt (52 bytes)
        base = Part.from_bytes(data, offset)
        extra = struct.unpack_from('<HHhhhhhh', data, offset + 48)
        return Belt(
            **base.__dict__,
            unknown_28=extra[0],
            unknown_30=extra[1],
            belt_connected_part_1=extra[2],
            belt_connected_part_2=extra[3],
            unknown_36_belt=extra[4],
            unknown_38=extra[5],
            unknown_40=extra[6],
            unknown_42=extra[7],
        ), 52
    elif part_type_value == PartType.ROPE:
        # Parse as Rope (54 bytes)
        base = Part.from_bytes(data, offset)
        extra = struct.unpack_from('<HHHHhhHHHH', data, offset + 48)
        return Rope(
            **base.__dict__,
            rope_segment_length=extra[0],
            unknown_28=extra[1],
            unknown_30=extra[2],
            unknown_32_rope=extra[3],
            rope_connected_part_1=extra[4],
            rope_connected_part_2=extra[5],
            part_1_connect_field_usage=extra[6],
            part_2_connect_field_usage=extra[7],
            unknown_44=extra[8],
            unknown_46=extra[9],
        ), 54
    elif part_type_value == PartType.PULLEY:
        # Parse as Pulley (56 bytes)
        base = Part.from_bytes(data, offset)
        extra = struct.unpack_from('<HHHh', data, offset + 48)
        return Pulley(
            **base.__dict__,
            unknown_28=extra[0],
            unknown_30=extra[1],
            unknown_32_pulley=extra[2],
            rope_index=extra[3],
        ), 56
    elif part_type_value == PartType.PROGRAMMABLE_BALL:
        # Parse as ProgrammableBall (60 bytes)
        base = Part.from_bytes(data, offset)
        extra = struct.unpack_from('<HHHHHH', data, offset + 48)
        return ProgrammableBall(
            **base.__dict__,
            density=extra[0],
            elasticity=extra[1],
            friction=extra[2],
            gravity_buoyancy=extra[3],
            mass=extra[4],
            appearance_2=extra[5],
        ), 60
    else:
        # Parse as regular Part (48 bytes)
        return Part.from_bytes(data, offset), 48


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
        # First 48 bytes using base Part structure
        base = struct.pack(
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
        # Extra 6 bytes specific to Rope: 3 H values
        extra = struct.pack('<HHH',
            self.rope_segment_length,
            self.unknown_28,
            self.unknown_30
        )
        return base + extra


@dataclass
class Pulley(Part):
    """Pulley part (56 bytes: 48 base + 8 extra)"""
    unknown_28: int = 0
    unknown_30: int = 0
    unknown_32_pulley: int = 1
    rope_index: int = -1

    def to_bytes(self) -> bytes:
        """Pack the pulley data into 56 bytes"""
        # First 48 bytes using base Part structure
        base = struct.pack(
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
        # Extra 8 bytes specific to Pulley: 4 H values
        extra = struct.pack('<HHHh',
            self.unknown_28,
            self.unknown_30,
            self.unknown_32_pulley,
            self.rope_index
        )
        return base + extra


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
        "position": {"x": part.pos_x, "y": part.pos_y}
    }
    
    # Only include flags if they differ from defaults
    default_f1, default_f2, default_f3 = get_default_part_flags(part.part_type)
    if part.flags_1 != default_f1:
        result["flags_1"] = flags1_to_list(part.flags_1)
    if part.flags_2 != default_f2:
        result["flags_2"] = flags2_to_list(part.flags_2)
    if part.flags_3 != default_f3:
        result["flags_3"] = flags3_to_list(part.flags_3)
    
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
    if part.belt_connect_pos_x != 0 or part.belt_connect_pos_y != 0 or part.belt_line_distance != 0 or part.unknown_32 != 0:
        result["belt_connection"] = {
            "x": part.belt_connect_pos_x,
            "y": part.belt_connect_pos_y,
            "distance": part.belt_line_distance
        }
        if part.unknown_32 != 0:
            result["belt_connection"]["unknown_32"] = part.unknown_32
    
    # Rope connections
    if part.rope_1_connect_pos_x != 0 or part.rope_1_connect_pos_y != 0:
        result["rope_1_connection"] = {
            "x": part.rope_1_connect_pos_x,
            "y": part.rope_1_connect_pos_y
        }
    if part.rope_2_connect_pos_x != 0 or part.rope_2_connect_pos_y != 0 or part.unknown_36 != 0:
        result["rope_2_connection"] = {
            "x": part.rope_2_connect_pos_x,
            "y": part.rope_2_connect_pos_y
        }
        if part.unknown_36 != 0:
            result["rope_2_connection"]["unknown_36"] = part.unknown_36
    
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
    
    # Convert flags - use defaults if not specified
    if "flags_1" in part_dict:
        flags_1 = list_to_flags1(part_dict["flags_1"])
    else:
        flags_1, _, _ = get_default_part_flags(part_type)
    
    if "flags_2" in part_dict:
        flags_2 = list_to_flags2(part_dict["flags_2"])
    else:
        _, flags_2, _ = get_default_part_flags(part_type)
    
    if "flags_3" in part_dict:
        flags_3 = list_to_flags3(part_dict["flags_3"])
    else:
        _, _, flags_3 = get_default_part_flags(part_type)
    
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
        "unknown_32": 0,
        "unknown_36": 0
    }
    
    # Belt connection
    if "belt_connection" in part_dict:
        bc = part_dict["belt_connection"]
        kwargs["belt_connect_pos_x"] = bc["x"]
        kwargs["belt_connect_pos_y"] = bc["y"]
        kwargs["belt_line_distance"] = bc["distance"]
        if "unknown_32" in bc:
            kwargs["unknown_32"] = bc["unknown_32"]
    
    # Rope connections
    if "rope_1_connection" in part_dict:
        rc = part_dict["rope_1_connection"]
        kwargs["rope_1_connect_pos_x"] = rc["x"]
        kwargs["rope_1_connect_pos_y"] = rc["y"]
    if "rope_2_connection" in part_dict:
        rc = part_dict["rope_2_connection"]
        kwargs["rope_2_connect_pos_x"] = rc["x"]
        kwargs["rope_2_connect_pos_y"] = rc["y"]
        if "unknown_36" in rc:
            kwargs["unknown_36"] = rc["unknown_36"]
    
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
    
    # Parse all parts (moving + fixed)
    normal_parts = []
    total_parts = num_moving + num_fixed
    for _ in range(total_parts):
        part, part_size = parse_part_from_bytes(data, offset)
        offset += part_size
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
        "music": music,
        "num_moving": num_moving  # Preserve this for round-trip conversion
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
    
    # Global settings - use num_moving from JSON if available, otherwise calculate from flags
    if "num_moving" in settings:
        num_moving = settings["num_moving"]
        num_fixed = len(parts) - num_moving
    else:
        # Backward compatibility: calculate from MOVING_PART flags
        num_moving = sum(1 for p in parts if p.flags_1 & Flags1.MOVING_PART)
        num_fixed = len(parts) - num_moving
    
    struct.pack_into('<hhHHHHHH', buffer, offset,
                     settings["pressure"], settings["gravity"],
                     settings.get("unknown_4", 0), settings.get("unknown_6", 0),
                     settings["music"], num_fixed, num_moving,
                     settings.get("unknown_14", 0))
    offset += 16
    
    # Write parts in their original order from JSON
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
    
    # Parse all parts (moving and fixed)
    print(f"\n{'='*60}")
    print(f"All Parts ({num_moving} moving + {num_fixed} fixed = {num_moving + num_fixed}):")
    print(f"{'='*60}")
    total_parts = num_moving + num_fixed
    for i in range(total_parts):
        part, part_size = parse_part_from_bytes(data, offset)
        offset += part_size
        
        part_category = "MOVING" if i < num_moving else "FIXED"
        print(f"\n  Part {i} ({part_category}): {get_part_type_name(part.part_type)} [{part_size} bytes]")
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
        
        # Type-specific fields
        if isinstance(part, Belt):
            if part.unknown_28 != 0:
                print(f"    Belt Unknown_28: {part.unknown_28}")
            if part.unknown_30 != 0:
                print(f"    Belt Unknown_30: {part.unknown_30}")
            if part.belt_connected_part_1 != -1:
                print(f"    Belt Connected Part 1: {part.belt_connected_part_1}")
            if part.belt_connected_part_2 != -1:
                print(f"    Belt Connected Part 2: {part.belt_connected_part_2}")
        elif isinstance(part, Rope):
            if part.rope_segment_length != 0:
                print(f"    Rope Segment Length: {part.rope_segment_length}")
            if part.rope_connected_part_1 != -1:
                print(f"    Rope Connected Part 1: {part.rope_connected_part_1}")
            if part.rope_connected_part_2 != -1:
                print(f"    Rope Connected Part 2: {part.rope_connected_part_2}")
        elif isinstance(part, Pulley):
            print(f"    Pulley unknown_28: {part.unknown_28}")
            print(f"    Pulley unknown_30: {part.unknown_30}")
            print(f"    Pulley unknown_32: {part.unknown_32_pulley}")
            if part.rope_index != -1:
                print(f"    Pulley rope_index: {part.rope_index}")
        elif isinstance(part, ProgrammableBall):
            print(f"    Density: {part.density}")
            print(f"    Elasticity: {part.elasticity}")
            print(f"    Friction: {part.friction}")
            print(f"    Gravity/Buoyancy: {part.gravity_buoyancy}")
            print(f"    Mass: {part.mass}")
    
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
    parser.add_argument('--output', type=str,
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
        
        # Check if input is a directory
        if input_path.is_dir():
            # Process all .TIM files in directory
            output_dir = Path(args.output) if args.output else input_path
            output_dir.mkdir(parents=True, exist_ok=True)
            
            tim_files = list(input_path.glob('*.TIM')) + list(input_path.glob('*.tim'))
            if not tim_files:
                print(f"No TIM files found in {input_path}")
                return
            
            print(f"Converting {len(tim_files)} TIM file(s) from {input_path}...")
            for tim_file in tim_files:
                output_file = output_dir / tim_file.with_suffix('.json').name
                print(f"  {tim_file.name} -> {output_file.name}")
                json_data = tim_to_json(str(tim_file))
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, indent=2, ensure_ascii=False)
            
            print(f"Saved {len(tim_files)} JSON file(s) to {output_dir}")
            return
        else:
            # Process single file
            if args.output:
                output_path = Path(args.output)
            else:
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
        
        # Check if input is a directory
        if input_path.is_dir():
            # Process all .json files in directory
            output_dir = Path(args.output) if args.output else input_path
            output_dir.mkdir(parents=True, exist_ok=True)
            
            json_files = list(input_path.glob('*.json'))
            if not json_files:
                print(f"No JSON files found in {input_path}")
                return
            
            print(f"Converting {len(json_files)} JSON file(s) from {input_path}...")
            for json_file in json_files:
                output_file = output_dir / json_file.with_suffix('.TIM').name
                print(f"  {json_file.name} -> {output_file.name}")
                with open(json_file, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                tim_bytes = json_to_tim(json_data)
                with open(output_file, 'wb') as f:
                    f.write(tim_bytes)
            
            print(f"Saved {len(json_files)} TIM file(s) to {output_dir}")
            return
        else:
            # Process single file
            if args.output:
                output_path = Path(args.output)
            else:
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
