from math import log10


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


if __name__ == "__main__":
    assert sum_invalids_in_range(11, 22) == 33
    assert sum_invalids_in_range(95, 115) == 99
    assert sum_invalids_in_range(998, 1012) == 1010