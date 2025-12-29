from dataclasses import dataclass


def get_ranges_and_ingredients(filename: str) -> tuple[list[tuple[int, int]], list[int]]:
    ranges = []
    ingredients = []
    range_mode = True
    with open(filename, 'r') as file:
        for line in file:
            stripped = line.strip()
            if not stripped:
                range_mode = False
                continue
            if range_mode:
                ranges.append(tuple(int(s) for s in stripped.split("-")))
            else:
                ingredients.append(int(stripped))
    return ranges, ingredients


def is_fresh(ingredient: int, ranges: list[tuple[int, int]]) -> bool:
    for start, end in ranges:
        if start <= ingredient <= end:
            return True
    return False


def count_fresh(ranges: list[tuple[int, int]], ingredients: list[int]) -> int:
    total = 0
    for ingredient in ingredients:
        if is_fresh(ingredient, ranges):
            total += 1
    return total


def count_all_fresh(ranges: list[tuple[int, int]]) -> int:
    points = sorted([RangePoint(num=r[0], is_start=True) for r in ranges] + [RangePoint(num=r[1], is_start=False) for r in ranges])

    total = 0
    last_start = None
    num_starts = 0
    for point in points:
        if point.is_start:
            num_starts += 1
            if last_start is None:
                last_start = point.num
        else:
            num_starts -= 1
            if num_starts == 0:
                total += point.num - last_start + 1
                last_start = None
    return total


@dataclass(frozen=True)
class RangePoint:
    num: int
    is_start: bool


    def __lt__(self, other: "RangePoint") -> bool:
        if self == other:
            return False
        if self.num == other.num:
            return self.is_start
        return self.num < other.num

if __name__ == '__main__':
    ranges, ingredients = get_ranges_and_ingredients("input.txt")
    # print(count_fresh(ranges, ingredients))
    print(count_all_fresh(ranges))