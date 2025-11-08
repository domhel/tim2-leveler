import struct
import math

def insert_bowlingball(buffer, offset, x, y) -> int:
    assert 0 <= x <= 560
    assert 0 <= y <= 377
    part_type_num_u16 = 9
    flags_1_u16 = 0x1000 #(moving part)
    flags_2_u16 = 0
    flags_3_u16 = 0x8008
    appearance_u16 = 0
    unknown_10_u16 = 0
    width_1_u16 = 0x20
    height_1_u16 = 0x20
    width_2_u16 = 0x20
    height_2_u16 = 0x20
    pos_x_i16 = x
    pos_y_i16 = y
    behavior_u16 = 0
    unknown_26_u16 = 0
    belt_connect_pos_x_u8 = 0
    belt_connect_pos_y_u8 = 0
    belt_line_distance_u16 = 0
    unknown_32_u16 = 0
    rope_1_connect_pos_x_u8 = 0
    rope_1_connect_pos_y_u8 = 0
    unknown_36_u16 = 0
    rope_2_connect_pos_x_u8 = 0
    rope_2_connect_pos_y_u8 = 0
    connected_1_i16 = -1
    connected_2_i16 = -1
    outlet_plugged_1_i16 = -1
    outlet_plugged_2_i16 = -1
    struct.pack_into('<HHHHHHHHHHhhHHBBHHBBHBBhhhh', buffer, offset, part_type_num_u16, flags_1_u16, flags_2_u16, flags_3_u16, appearance_u16, unknown_10_u16, width_1_u16, height_1_u16, width_2_u16, height_2_u16, pos_x_i16, pos_y_i16, behavior_u16, unknown_26_u16, belt_connect_pos_x_u8, belt_connect_pos_y_u8, belt_line_distance_u16, unknown_32_u16, rope_1_connect_pos_x_u8, rope_1_connect_pos_y_u8, unknown_36_u16, rope_2_connect_pos_x_u8, rope_2_connect_pos_y_u8, connected_1_i16, connected_2_i16, outlet_plugged_1_i16, outlet_plugged_2_i16)
    return offset + 48

def main():
    num_parts_48_size = 150
    buffer=bytearray(226 + 48*num_parts_48_size)
    offset=0
    #Magic number
    struct.pack_into('>I', buffer, offset, 0xEFAC1301)
    offset+=4
    #Background
    struct.pack_into('>H', buffer, offset, 0x0003)
    offset+=2
    #Quiz title
    quiz_title=b'BOWLING_BALL\0'
    quiz_title_len=len(quiz_title)
    struct.pack_into(f'<{quiz_title_len}s', buffer, offset, quiz_title)
    offset+=quiz_title_len
    #Goal description
    goal_description=b'\0'
    goal_description_len=len(goal_description)
    struct.pack_into(f'<{goal_description_len}s', buffer, offset, goal_description)
    offset+=goal_description_len
    #Hints. 2 byte num hints, (7 byte per empty hint (x_u16,y_u16,flip_u16,text\0)), 8 hints even if empty
    hints_bytes_skip=2+7*8
    offset+=hints_bytes_skip
    #Global puzzle information
    pressure_i16 = 67
    gravity_i16 = 272
    unknown_4_u16 = unknown_6_u16 = 0
    music_u16 = 1000 #1000-1023
    num_parts_fixed_u16 = 0
    num_parts_moving_u16 = num_parts_48_size
    unknown_14_u16 = 0
    struct.pack_into('<hhHHHHHH', buffer, offset, pressure_i16, gravity_i16, unknown_4_u16, unknown_6_u16, music_u16, num_parts_fixed_u16, num_parts_moving_u16, unknown_14_u16)
    offset+=16
    #Bowling Ball
    for i in range(num_parts_48_size):
        num_rounds = 3
        angle = i / num_parts_48_size * 2 * math.pi * num_rounds
        radius_min = 20
        radius_max = 150
        center_x = 300
        center_y = 150
        radius = int(radius_min + (radius_max - radius_min) * (i / num_parts_48_size))
        x = int(center_x + radius * math.cos(angle))
        y = int(center_y + radius * math.sin(angle))
        offset = insert_bowlingball(buffer, offset, x, y)
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

    assert offset == len(buffer)

    print(buffer.hex(' ', bytes_per_sep=2))

    filename = 'GENERATED0001.TIM'
    with open(filename, 'wb') as file:
        file.write(buffer)

    #Readback to be sure
    with open(filename, 'rb') as file:
        file_content = file.read()
        assert len(file_content) == len(buffer)
        assert file_content == buffer


if __name__ == "__main__":
    main()
