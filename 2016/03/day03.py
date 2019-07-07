def get_sides():
    with open('input.txt') as file:
        for line in file:
            yield [int(x) for x in line.split()]

def get_sides_columns():
    buffer = []
    with open('input.txt') as file:
        for i, line in enumerate(file):
            buffer.append([int(x) for x in line.split()])
            if len(buffer) == 3:
                yield [buffer[0][0], buffer[1][0], buffer[2][0]]
                yield [buffer[0][1], buffer[1][1], buffer[2][1]]
                yield [buffer[0][2], buffer[1][2], buffer[2][2]]
                buffer = []

def get_possible_triangles():
    num_possible = 0
    for sides in get_sides_columns():
        if sides[0] + sides[1] > sides[2] and sides[1] + sides[2] > sides[0] and sides[0] + sides[2] > sides[1]:
            num_possible += 1
    return num_possible

print(get_possible_triangles())
