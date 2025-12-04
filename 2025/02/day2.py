from math import log10

def is_invalid(num: int) -> bool:
    as_string = str(num)
    length = len(as_string)
    if length < 2 or length % 2 != 0:
        return False

    return as_string[:length] == as_string[length]


def sum_invalids_in_range(start: int, end: int) -> int:
    cur = start
    target = 0
    total = 0
    while cur <= end:
        print(f"cur: {cur}")
        num_digits = int(log10(cur)) + 1
        if num_digits % 2 != 0:
            cur = 10 ** (num_digits + 1)
            if cur > end:
                return total

        first_half = cur // (10 ** (num_digits // 2))
        if cur == target:
            total += cur
            # find next first half
        else:
            target = first_half * (10 ** (num_digits // 2)) + first_half
            
        if target <= cur:
            next_first_half = first_half + 1
            
            target = next_first_half * (10 ** (num_digits // 2))
        cur = target
    return total
