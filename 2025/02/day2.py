from math import log10


def sum_ranges_in_file(filename: str) -> int:
    with open(filename, 'r') as file:
        content = file.read()
        total = 0
        for rng in content.split(","):
            parts = rng.split("-")
            total += sum(get_invalids_in_range(int(parts[0]), int(parts[1]), 2))
        return total



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




def get_invalids_in_range(start: int, end: int, num_repeats: int = 2) -> set[int]:
    cur = start
    invalids = set()
    while cur <= end:
        num_digits = int(log10(cur)) + 1
        if num_digits % num_repeats != 0:
            cur = 10 ** num_digits
            continue

        segment_length = num_digits // num_repeats
        first_repeat = cur // (10 ** (num_digits - segment_length))
        target = 0
        for i in range(num_repeats):
            target += first_repeat * (10 ** (segment_length * i))

        if cur == target:
            invalids.add(cur)
            # find next first half

        if target <= cur:
            next_first_repeat = first_repeat + 1
            target = 0
            for i in range(num_repeats):
                target += next_first_repeat * (10 ** (segment_length * i))

        cur = target
    return invalids


if __name__ == "__main__":
    assert get_invalids_in_range(11, 22) == {11, 22}
    assert get_invalids_in_range(95, 115) == {99}
    assert get_invalids_in_range(998, 1012) == {1010}
    assert get_invalids_in_range(1188511880, 1188511890) == {1188511885}
    assert get_invalids_in_range(222220, 222224) == {222222}
    assert get_invalids_in_range(1698522,1698528) == set()
    assert get_invalids_in_range(446443, 446449) == {446446}
    assert get_invalids_in_range(38593856, 38593862) == {38593859}
    print(sum_ranges_in_file("input.txt"))