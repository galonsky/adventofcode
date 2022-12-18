import re
from collections import defaultdict
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


def get_spots_just_outside(sensor: tuple[int, int], beacon: [int, int], max_dim: int) -> Generator[tuple[int, int], None, None]:
    beacon_distance = distance(sensor, beacon) + 1
    # find all the points (beacon_distance + 1) from sensor

    for x in range(beacon_distance + 1):
        y = beacon_distance - x
        yield sensor[0] + x, sensor[1] + y
        yield sensor[0] - x, sensor[1] + y
        yield sensor[0] + x, sensor[1] - y
        yield sensor[0] - x, sensor[1] - y


def find_tuning_frequency(sensor_and_beacons: list[tuple[tuple[int, int], tuple[int, int]]], max_dim: int) -> int:
    candidates = defaultdict(int)
    # get all the points in the "rings" just outside of sensor reach, and keep track of the number of intersections
    for sensor, beacon in sensor_and_beacons:
        spots = get_spots_just_outside(sensor, beacon, max_dim)
        for spot in spots:
            if 0 <= spot[0] <= max_dim and 0 <= spot[1] <= max_dim:
                candidates[spot] += 1

    max_no_intersections = max(candidates.values())

    # there will be ties for number of intersections, so find the one that is actually not in range of sensors
    for spot in [c for c in candidates if candidates[c] == max_no_intersections]:
        success = True
        for sensor, beacon in sensor_and_beacons:
            beacon_distance = distance(sensor, beacon)
            sensor_to_spot = distance(sensor, spot)
            if sensor_to_spot <= beacon_distance:
                success = False
                break
        if success:
            return 4000000 * spot[0] + spot[1]



if __name__ == '__main__':
    # sensor_data = get_sensor_and_beacon_pairs("input.txt")
    # print(get_num_no_beacons_on_line(sensor_data, 2000000))
    sensor_data = list(get_sensor_and_beacon_pairs("input.txt"))
    # print(get_num_no_beacons_on_line(sensor_data, 10))
    print(find_tuning_frequency(sensor_data, 4000000))
