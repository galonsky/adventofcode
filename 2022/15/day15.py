import re
from typing import Generator, Iterable

PATTERN = re.compile(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)')


def get_sensor_and_beacon_pairs(filename: str) -> Generator[tuple[tuple[int, int], tuple[int, int]], None, None]:
    with open(filename, 'r') as file:
        for line in file:
            match = PATTERN.match(line.strip())
            yield (int(match.group(1)), int(match.group(2))), (int(match.group(3)), int(match.group(4)))


def distance(a: tuple[int, int], b: tuple[int, int]) -> int:
    return abs(b[0] - a[0]) + abs(b[1] - a[1])


def get_num_no_beacons_on_line(sensor_and_beacons: Iterable[tuple[tuple[int, int], tuple[int, int]]], y: int) -> int:
    candidates: set[int] = set()
    beacons = []
    for sensor, beacon in sensor_and_beacons:
        beacons.append(beacon)
        beacon_distance = distance(sensor, beacon)
        distance_to_line = abs(sensor[1] - y)
        if distance_to_line > beacon_distance:
            continue

        candidates.add(sensor[0])
        distance_each_side = beacon_distance - distance_to_line
        for i in range(sensor[0] + 1, sensor[0] + distance_each_side + 1):
            candidates.add(i)
        for i in range(sensor[0] - 1, sensor[0] - distance_each_side - 1, -1):
            candidates.add(i)

    for beacon in beacons:
        if beacon[1] == y and beacon[0] in candidates:
            candidates.remove(beacon[0])

    return len(candidates)


if __name__ == '__main__':
    sensor_data = get_sensor_and_beacon_pairs("input.txt")
    print(get_num_no_beacons_on_line(sensor_data, 2000000))
    # sensor_data = get_sensor_and_beacon_pairs("sample.txt")
    # print(get_num_no_beacons_on_line(sensor_data, 10))
