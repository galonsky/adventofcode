from typing import Callable


VECTORS = (
    (-1, -1),
    (0, -1),
    (1, -1),
    (-1, 0),
    (0, 0),
    (1, 0),
    (-1, 1),
    (0, 1),
    (1, 1),
)


def get_neighbors_as_int(x: int, y: int, getter: Callable[[int, int], bool]) -> int:
    bin_str = ""
    for dx, dy in VECTORS:
        newx = x + dx
        newy = y + dy
        bin_str += "1" if getter(newx, newy) else "0"
    return int(bin_str, 2)



def get_algo_and_image(filename: str) -> tuple[str, dict[tuple[int, int], bool]]:
    with open(filename, 'r') as file:
        line_iter = iter(file)
        algo = next(line_iter)
        next(line_iter)
        image = dict()
        for y, line in enumerate(line_iter):
            for x, ch in enumerate(line.strip()):
                image[(x, y)] = ch == "#"
        return algo, image


def enhance(image: dict[tuple[int, int], bool], algo: str, default: bool = False) -> dict[tuple[int, int]]:
    min_x = min(coord[0] for coord in image.keys()) - 1
    max_x = max(coord[0] for coord in image.keys()) + 1
    min_y = min(coord[1] for coord in image.keys()) - 1
    max_y = max(coord[1] for coord in image.keys()) + 1

    new_image = {}
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            neighbors_int = get_neighbors_as_int(x, y, lambda *coord: image.get(coord, default))
            new_val = algo[neighbors_int] == "#"
            new_image[(x, y)] = new_val
    return new_image


def print_image(image: dict[tuple[int, int], bool]):
    min_x = min(coord[0] for coord in image.keys())
    max_x = max(coord[0] for coord in image.keys())
    min_y = min(coord[1] for coord in image.keys())
    max_y = max(coord[1] for coord in image.keys())

    for y in range(min_y, max_y + 1):
        line = ""
        for x in range(min_x, max_x + 1):
            line += "#" if image[(x, y)] else "."
        print(line)

    print()


def count_lit_pixels(image: dict[tuple[int, int], bool]) -> int:
    return len([
        key for key in image.keys() if image[key]
    ])


if __name__ == '__main__':
    algo, image = get_algo_and_image("input.txt")
    # print(algo)
    default = False
    for _ in range(50):
        image = enhance(image, algo, default)
        default = not default
    # print_image(image)
    # image = enhance(image, algo)
    # print_image(image)
    # image = enhance(image, algo, True)
    # print_image(image)
    print(count_lit_pixels(image))
    # 5834 too low