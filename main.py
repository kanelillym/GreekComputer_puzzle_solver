# Globals to avoid burying hardcoded magic numbers
SPOKE_COUNT = 12
RING_COUNT = 4
PLATE_COUNT = 5
TARGET_SPOKE_SUM = 42

# This data is taken from the physical puzzle.
# Each 'plate' array is treated as an array of 4 circular arrays.
# plate4 is the top plate, plate1 is the bottom, and the baseplate is functionally fixed in place.
plate4 =    [[7,  0,  15, 0,  8,  0,  3,  0,  6,  0,  10, 0],
             [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]]

plate3 =    [[0,  6,  17, 7,  3,  0,  6,  0,  11, 11, 6,  11],
             [0,  12, 0,  4,  0,  7,  15, 0,  0,  14, 0,  9],
             [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]]

plate2 =    [[0,  7,  8,  9,  13, 9,  7,  13, 21, 17, 4,  5],
             [1,  12, 0,  21, 6,  15, 4,  9,  18, 11, 26, 14],
             [0,  9,  0,  5,  0,  10, 0,  8,  0,  22, 0,  16],
             [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]]

plate1 =    [[0,  7,  14, 11, 0,  8,  0,  16, 2,  7,  0,  9],
             [3,  6,  0,  14, 12, 3,  8,  9,  0,  9,  20, 12],
             [0,  2,  13, 9,  0,  17, 19, 3,  12, 3,  26, 6],
             [0,  12, 0,  6,  0,  10, 0,  10, 0,  1,  0,  9]]

baseplate = [[14, 11, 11, 14, 11, 14, 11, 14, 14, 11, 14, 11],
             [15, 4,  5,  6,  7,  8,  9,  10, 11, 12, 13, 14],
             [9,  4,  4,  6,  6,  3,  3,  14, 14, 21, 21, 9],
             [8,  8,  3,  4,  12, 2,  5,  10, 7,  16, 8,  7]]

plate_rotations = [0]*PLATE_COUNT

data = [baseplate, plate1, plate2, plate3, plate4]


##############################################


def read_value_at_position_on_target_plate(plate_number, pos_y, pos_x):
    adjusted_pos_x = (pos_x + plate_rotations[plate_number]) % SPOKE_COUNT
    return data[plate_number][pos_y][adjusted_pos_x]


def read_value_at_position(pos_y, pos_x):
    result = 0
    target_plate = PLATE_COUNT - 1 # top plate accounting for 0 indexing
    while(result == 0):
        result = read_value_at_position_on_target_plate(target_plate, pos_y, pos_x)
        target_plate = target_plate - 1
    return result


def rotate_plate(plate_number, rotation_amount=1):
    plate_rotations[plate_number] += rotation_amount


def calculate_spoke_sum(target_spoke):
    sum = 0
    for i in range(0, RING_COUNT):
        sum += read_value_at_position(i, target_spoke)
    return sum


def all_spokes_equal_target_sum():
    spoke_sums = [0]*SPOKE_COUNT
    for i in range(0, SPOKE_COUNT):
        spoke_sums[i] = calculate_spoke_sum(i)
    return spoke_sums == [TARGET_SPOKE_SUM]*SPOKE_COUNT


def spin_incrementally():
    # Rotate the top plate one position. If it's been rotated through all positions, reset it and rotate the plate below it.
    plate_to_rotate = PLATE_COUNT - 1 # account for 0-indexing
    while True:
        plate_rotations[plate_to_rotate] += 1
        if plate_rotations[plate_to_rotate] >= SPOKE_COUNT:
            plate_rotations[plate_to_rotate] = 0
            plate_to_rotate -= 1
            continue
        break


def all_permutations_have_been_tested():
    # All permutations can be tried without spinning the baseplate. If the baseplate rotation is incremented, the puzzle must be unsolvable.
    return plate_rotations[0] != 0


def conclude_as_failure():
    print("The answer could not be found.")


def print_all_cell_values():
    for y in range(0, RING_COUNT):
        for x in range(0, SPOKE_COUNT):
            print("{val:2d}".format(val = read_value_at_position(y, x)), end='  ')
        print("")


def print_all_spoke_sums():
    for i in range(0, SPOKE_COUNT):
        print("{sum:2d}".format(sum=calculate_spoke_sum(i)), end='  ')


def conclude_as_success():
    print("Answer found!\nThe correct plate rotations are", plate_rotations, "and the final values in each position are:\n")
    print_all_cell_values()
    print("---------------------------------------------")
    print_all_spoke_sums()


def main():
    while(all_spokes_equal_target_sum() == False):
        spin_incrementally()
        if(all_permutations_have_been_tested()):
            conclude_as_failure()
            return
    # Exiting while loop: all_spokes_equal_target_sum() == True
    conclude_as_success()


if __name__ == '__main__':
    main()
