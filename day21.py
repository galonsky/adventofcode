import re

rule_re = re.compile('(.+) =\> (.+)')


def flip_horizontal(pic):
    return [list(reversed(arr)) for arr in pic]


def rotate_90(pic):
    rotated = []
    reversed_pic = pic[::-1]
    for i in range(len(pic)):
        rotated.append([line[i] for line in reversed_pic])
    return rotated


def print_pic(pic):
    for line in pic:
        print(''.join(line))
    print()


def to_pic(string):
    parts = string.split('/')
    return [list(part) for part in parts]


def to_str(pic):
    return '/'.join([''.join(line) for line in pic])


def get_equivalents(string):
    equivs = set()
    equivs.add(string)

    pic = to_pic(string)
    pic = rotate_90(pic)
    equivs.add(to_str(pic))

    pic = rotate_90(pic)
    equivs.add(to_str(pic))

    pic = rotate_90(pic)
    equivs.add(to_str(pic))

    pic = to_pic(string)
    pic = flip_horizontal(pic)
    equivs.add(to_str(pic))

    pic = rotate_90(pic)
    equivs.add(to_str(pic))

    pic = rotate_90(pic)
    equivs.add(to_str(pic))

    pic = rotate_90(pic)
    equivs.add(to_str(pic))

    return equivs


pic = [
    ['.', '#', '.'],
    ['.', '.', '#'],
    ['#', '#', '#']]

with open('day21_input.txt') as file:
    rules = [line.rstrip('\n') for line in file]
# rules = ['../.# => ##./#../...', '.#./..#/### => #..#/..../..../#..#']
rule_dict = {}

for rule in rules:
    groups = rule_re.match(rule).groups()
    for equiv in get_equivalents(groups[0]):
        rule_dict[equiv] = groups[1]

for iter in range(18):
    print(iter)
    oldsize = len(pic)
    if oldsize % 2 == 0:
        a = 2
        b = 3
    elif oldsize % 3 == 0:
        a = 3
        b = 4

    newsize = oldsize * b // a
    enlargements = []
    for row in range(0, oldsize, a):
        for col in range(0, oldsize, a):
            block = [line[col:col + a] for line in pic[row:row + a]]
            block_str = to_str(block)
            enlargement_str = rule_dict[block_str]
            enlargements.append(to_pic(enlargement_str))
    newpic = []
    for i in range(newsize):
        line = []
        for j in range(newsize):
            enlargement_idx = (i // b) * (newsize // b) + j // b
            line.append(enlargements[enlargement_idx][i % b][j % b])
        newpic.append(line)
    # print_pic(newpic)
    pic = newpic

print(to_str(pic).count('#'))

# 000111
# 000111
# 000111
# 222333
# 222333
# 222333


# print_pic(pic)
# print_pic(flip_horizontal(pic))
# print_pic(rotate_90(pic))
# print_pic(rotate_90(rotate_90(pic)))
# print_pic(rotate_90(rotate_90(rotate_90(pic))))
# print_pic(rotate_90(rotate_90(rotate_90(rotate_90(pic)))))

# print_pic(flip_horizontal(rotate_90(rotate_90(pic))))
