def get_directions():
    with open('input.txt') as file:
        return file.read().split(', ')
        
def get_distance():
    directions = get_directions()
    orientations = ['n', 'e', 's', 'w']
    current_orientation = 0
    visited_locations = set()
    x, y = (0, 0)
    visited_locations.add((x, y))
    for direction in directions:
        if direction[0] == 'L':
            current_orientation = (current_orientation - 1) % 4
        else:
            current_orientation = (current_orientation + 1) % 4
        magnitude = int(direction[1:])
        
        y_delta = 0
        x_delta = 0
        
        if current_orientation == 0:
            y_delta = magnitude
        elif current_orientation == 1:
            x_delta = magnitude
        elif current_orientation == 2:
            y_delta = -magnitude
        else:
            x_delta = -magnitude
        
        for i in range(abs(y_delta)):
            y += 1 if y_delta >=0 else -1
            if (x, y) in visited_locations:
                return abs(x) + abs(y)
            visited_locations.add((x, y))
        for i in range(abs(x_delta)):
            x += 1 if x_delta >= 0 else -1
            if (x, y) in visited_locations:
                return abs(x) + abs(y)
            visited_locations.add((x, y))
    #return abs(x) + abs(y)

print(get_distance())
