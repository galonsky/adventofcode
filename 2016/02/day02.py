def get_lines(filename):
    with open(filename) as file:
        for line in file:
            yield line.strip()

numpad = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],    
]

new_numpad = [
    [None, None, 1, None, None],
    [None, 2, 3, 4, None],
    [5, 6, 7, 8, 9],
    [None, 'A', 'B', 'C', None],
    [None, None, 'D', None, None],
]

def get_code(filename):
    code = ""
    x = 1
    y = 1
    for line in get_lines(filename):
        for ch in line:
            if ch == 'U' and y >= 1:
                y -= 1
            elif ch == 'D' and y <= 1:
                y += 1
            elif ch == 'L' and x >= 1:
                x -= 1
            elif ch == 'R' and x <= 1:
                x += 1
        code += str(numpad[y][x])
    return code

def is_valid(x, y):
    if x < 0 or y < 0:
        return False
    if x > 4 or y > 4:
        return False
    if new_numpad[y][x] is None:
        return False
    return True

def get_code2(filename):
    code = ""
    x = 0
    y = 2
    for line in get_lines(filename):
        for ch in line:
            if ch == 'U' and is_valid(x, y -1):
                y -= 1
            elif ch == 'D' and is_valid(x, y + 1):
                y += 1
            elif ch == 'L' and is_valid(x - 1, y):
                x -= 1
            elif ch == 'R' and is_valid(x + 1, y):
                x += 1
        code += str(new_numpad[y][x])
    return code
print(get_code2('input.txt'))
            
