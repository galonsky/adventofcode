from math import log10


def sum_ranges_in_file(filename: str) -> int:
    with open(filename, 'r') as file:
        content = file.read()
        total = 0
        for rng in content.split(","):
            parts = rng.split("-")
            invalids = get_invalids_in_range(int(parts[0]), int(parts[1]))
            print(f"start={parts[0]}, end={parts[1]}, invalids={invalids})")
            total += sum(invalids)
        return total



# part 1
def sum_invalids_in_range(start: int, end: int) -> int:
    cur = start
    target = 0
    total = 0
    while cur <= end:
        print(f"cur: {cur}")
        num_digits = int(log10(cur)) + 1
        # print(f"num digits: {num_digits}")
        if num_digits % 2 != 0:
            cur = 10 ** (num_digits)
            print(f"new cur: {cur}")
            continue

        first_half = cur // (10 ** (num_digits // 2))
        target = first_half * (10 ** (num_digits // 2)) + first_half

        print(f"first half: {first_half}")
        print(f"new target: {target}")

        if cur == target:
            total += cur
            # find next first half
        
        if target <= cur:
            next_first_half = first_half + 1
            target = next_first_half * (10 ** (num_digits // 2)) + next_first_half
            

        cur = target
    return total



# part 2
def get_invalids_in_range(start: int, end: int) -> set[int]:
    cur = start
    invalids = set()
    while cur <= end:
        num_digits = int(log10(cur)) + 1
        num_repeat_options = [i for i in range(2, num_digits+1) if num_digits % i == 0]
        if not num_repeat_options:
            cur = 10 ** num_digits
            continue

        targets = set()
        for num_repeats in num_repeat_options:
            segment_length = num_digits // num_repeats
            first_repeat = cur // (10 ** (num_digits - segment_length))
            target = 0
            for i in range(num_repeats):
                target += first_repeat * (10 ** (segment_length * i))
            targets.add(target)

        if cur in targets:
            invalids.add(cur)

        # add target for the next prefix that will be the lowest number
        smallest_num_repeat = num_repeat_options[0]
        segment_length = num_digits // smallest_num_repeat
        first_repeat = cur // (10 ** (num_digits - segment_length))
        targets.add((first_repeat + 1) * (10 ** (num_digits - segment_length)))

        cur = min([target for target in targets if target > cur])
    return invalids


if __name__ == "__main__":
    # assert get_invalids_in_range(11, 22) == {11, 22}
    # assert get_invalids_in_range(95, 115) == {99, 111}
    # assert get_invalids_in_range(998, 1012) == {999, 1010}
    # assert get_invalids_in_range(1188511880, 1188511890) == {1188511885}
    # assert get_invalids_in_range(222220, 222224) == {222222}
    # assert get_invalids_in_range(1698522,1698528) == set()
    # assert get_invalids_in_range(446443, 446449) == {446446}
    # assert get_invalids_in_range(38593856, 38593862) == {38593859}
    # assert get_invalids_in_range(565653, 565659) == {565656}
    # assert get_invalids_in_range(824824821, 824824827) == {824824824}
    # assert get_invalids_in_range(2121212118, 2121212124) == {2121212121}
    # assert get_invalids_in_range(942, 1466) == {1010, 1111, 999, 1212, 1313, 1414}
    print(get_invalids_in_range(1493, 2439))
    assert get_invalids_in_range(1493, 2439) == {2020, 1515, 2222, 1616, 2323, 1717, 2424, 1818, 1919, 2121}
    print(sum_ranges_in_file("input.txt"))
    # 44818202937 too low