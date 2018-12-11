from collections import defaultdict


def get_hundreths_digit(n):
    if n < 100:
        return 0
    return int(str(n // 100)[-1])

def get_power_level(x, y, serial):
    rack_id = x + 10
    power = rack_id * y
    power += serial
    power *= rack_id
    power = get_hundreths_digit(power)
    power = power - 5
    return power

def get_powers(serial):
    powers = defaultdict(dict)
    for x in range(1, 301):
        for y in range(1, 301):
            powers[x][y] = get_power_level(x, y, serial)
    return powers

def get_highest_power_square(powers, square_size=3):

    square_powers_by_size = {1: powers}
    for size in range(2, square_size + 1):
        square_powers = get_square_powers_fast(square_powers_by_size, size)
        square_powers_by_size[size] = square_powers

    return get_max_coords_and_powers(square_powers_by_size[square_size])

def get_max_coords_and_powers(square_powers):
    max_power = 0
    max_coords = (0,0)
    for x, y_dict in square_powers.items():
        for y, power in y_dict.items():
            if power > max_power:
                max_power = power
                max_coords = (x, y)
    return max_coords, max_power

def get_square_powers_fast(square_powers_by_size, square_size):
    
    powers = square_powers_by_size[1]
    last_square_powers = square_powers_by_size[square_size - 1]
    square_powers = defaultdict(dict)
    for x_start in range(1, 301 - square_size + 1):
        for y_start in range(1, 301 - square_size + 1):
            square_power = last_square_powers[x_start][y_start] + last_square_powers[x_start + 1][y_start + 1]
            square_power += powers[x_start][y_start + square_size - 1]
            square_power += powers[x_start + square_size - 1][y_start]
            if square_size > 2:
                square_power -= square_powers_by_size[square_size - 2][x_start + 1][y_start + 1]
            square_powers[x_start][y_start] = square_power

    return square_powers

def get_highest_square_of_any_size(serial):
    powers = get_powers(serial)
    square_powers_by_size = {1: powers}
    max_power = 0
    max_coords = (0, 0)
    max_size = 0
    last_square_powers = powers
    for size in range(2, 301):
        print(size)
        square_powers = get_square_powers_fast(square_powers_by_size, size)
        coords, power = get_max_coords_and_powers(square_powers)
        if power > max_power:
            max_power = power
            max_coords = coords
            max_size = size
        square_powers_by_size[size] = square_powers
    return (max_coords[0], max_coords[1], max_size)


# assert get_power_level(3, 5, 8) == 4
# assert get_power_level(122, 79, 57) == -5
# assert get_power_level(217, 196, 39) == 0
# assert get_power_level(101, 153, 71) == 4
# powers = get_powers(9435)
print(get_highest_square_of_any_size(9435))
