import re
from collections import Counter
from typing import Iterable

PATTERN = re.compile(r'((?:[a-z]+-)+)(\d+)\[([a-z]+)]')


def get_rooms(filename: str) -> Iterable[str]:
    with open(filename, 'r') as file:
        for line in file:
            yield line.rstrip('\n')


def part1():
    real_rooms = 0
    rooms = get_rooms('input.txt')
    for room in rooms:
        match = PATTERN.match(room)
        encrypted, room_id, checksum = match.groups()
        counter = Counter()
        for ch in encrypted:
            if ch == '-':
                continue
            counter[ch] += 1
        most_common_then_alphabetical = sorted(counter.most_common(), key=lambda tu: (-tu[1], tu[0]))[:5]
        most_common_set = {t[0] for t in most_common_then_alphabetical}
        if most_common_set == set(checksum):
            real_rooms += int(room_id)
    return real_rooms


def decrypt(encrypted: str, sector_id: int) -> str:
    decrypted = ''
    for ch in encrypted:
        if ch == '-':
            decrypted += ' '
        else:
            decrypted += chr((ord(ch) + sector_id - ord('a')) % 26 + ord('a'))
    return decrypted


def part2():
    rooms = get_rooms('input.txt')
    for room in rooms:
        match = PATTERN.match(room)
        encrypted, room_id, checksum = match.groups()
        print(decrypt(encrypted, int(room_id)), room_id)



if __name__ == '__main__':
    part2()
