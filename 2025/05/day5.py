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


if __name__ == '__main__':
    ranges, ingredients = get_ranges_and_ingredients("input.txt")
    print(count_fresh(ranges, ingredients))