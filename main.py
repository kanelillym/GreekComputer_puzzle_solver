SPOKE_COUNT = 12
TARGET_SPOKE_SUM = 42
TIER_COUNT = 4

# This data is taken from the physical puzzle
ring4 = [[7,  0,  15, 0,  8,  0,  3,  0,  6,  0,  10, 0],
         [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
         [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
         [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]]

ring3 = [[0,  6,  17, 7,  3,  0,  6,  0,  11, 11, 6,  11],
         [0,  12, 0,  4,  0,  7,  15, 0,  0,  14, 0,  9],
         [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
         [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]]

ring2 = [[0,  7,  8,  9,  13, 9,  7,  13, 21, 17, 4,  5],
         [1,  12, 0,  21, 6,  15, 4,  9,  18, 11, 26, 14],
         [0,  9,  0,  5,  0,  10, 0,  8,  0,  22, 0,  16],
         [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]]

ring1 = [[0,  7,  14, 11, 0,  8,  0,  16, 2,  7,  0,  9],
         [3,  6,  0,  14, 12, 3,  8,  9,  0,  9,  20, 12],
         [0,  2,  13, 9,  0,  17, 19, 3,  12, 3,  26, 6],
         [0,  12, 0,  6,  0,  10, 0,  10, 0,  1,  0,  9]]

plate = [[14, 11, 11, 14, 11, 14, 11, 14, 14, 11, 14, 11],
         [15, 4,  5,  6,  7,  8,  9,  10, 11, 12, 13, 14],
         [9,  4,  4,  6,  6,  3,  3,  14, 14, 21, 21, 9],
         [8,  8,  3,  4,  12, 2,  5,  10, 7,  16, 8,  7]]

ring_rotations = [0, 0, 0, 0, 0]

data = [plate, ring1, ring2, ring3, ring4]


##############################################


def read_from_ring(ring_number, pos_y, pos_x):
    adjusted_pos_x = (pos_x + ring_rotations[ring_number]) % SPOKE_COUNT
    return data[ring_number][pos_y][adjusted_pos_x]


def read_position(pos_y, pos_x):
    result = 0
    target_ring = 4
    while(result == 0):
        result = read_from_ring(target_ring, pos_y, pos_x)
        target_ring = target_ring - 1
    return result


def rotate_ring(ring_number, rotation_amount=1):
    ring_rotations[ring_number] += rotation_amount


def calculate_spoke_sum(spoke_number):
    sum = 0
    for i in range(0, TIER_COUNT):
        sum += read_position(i, spoke_number)
    return sum


def all_spokes_equal_target_sum():
    spoke_sums = [0]*SPOKE_COUNT
    for i in range(0, SPOKE_COUNT):
        spoke_sums[i] = calculate_spoke_sum(i)
    return spoke_sums == [TARGET_SPOKE_SUM]*SPOKE_COUNT


def spin_incrementally():
    ring_to_rotate = 4
    while True:
        ring_rotations[ring_to_rotate] += 1
        if ring_rotations[ring_to_rotate] >= SPOKE_COUNT: # The ring has been spun fully around, rotate the next one down
            ring_rotations[ring_to_rotate] = 0
            ring_to_rotate -= 1
            continue
        break


def main():
    while(all_spokes_equal_target_sum() == False):
        spin_incrementally()
        if(ring_rotations[0] != 0):
            print("The answer could not be found.")
            return
    print("Answer found!\nThe correct ring rotations are", ring_rotations, "and the final values in each position are:\n")
    print_all_values()
    print("---------------------------------------------")
    for i in range(0, SPOKE_COUNT):
        print(calculate_spoke_sum(i), end='  ')


def print_all_values():
    for y in range(0, TIER_COUNT):
        for x in range(0, SPOKE_COUNT):
            print("{val:2d}".format(val = read_position(y, x)), end='  ')
        print("")

if __name__ == '__main__':
    main()
