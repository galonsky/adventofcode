from typing import Generator


def get_word_search(filename: str) -> list[str]:
    with open(filename, 'r') as file:
        return [line.strip() for line in file]


def get_all_3_by_3(ws: list[str]) -> Generator[list[str], None, None]:
    height = len(ws)
    width = len(ws[0])
    for y in range(height - 2):
        for x in range(width - 2):
            yield [ws[y+i][x:x+3] for i in range(3)]


def diag(ws: list[str], startx: int, starty: int, dx: int, dy: int) -> str:
    res = ""
    x = startx
    y = starty
    while len(ws[0]) > x >= 0 and len(ws) > y >= 0:
        res += ws[y][x]
        x += dx
        y += dy
    return res


def get_all_lines(ws: list[str]) -> Generator[str, None, None]:
    height = len(ws)
    width = len(ws[0])

    for line in ws:
        yield line
    for x in range(width):
        yield ''.join([ws[y][x] for y in range(height)])
    # main diagonal, x and y increase each time
    yield diag(ws, 0, 0, 1, 1)
    for i in range(1, width):
        yield diag(ws, i, 0, 1, 1)
    for i in range(1, height):
        yield diag(ws, 0, i, 1, 1)

    # anti diagonal, x decreases, and y increase each time
    yield diag(ws, width - 1, 0, -1, 1)
    for i in range(0, width - 1):
        yield diag(ws, i, 0, -1, 1)
    for i in range(1, height):
        yield diag(ws, width - 1, i, -1, 1)


def get_all_xmas(ws: list[str]) -> int:
    total = 0
    for line in get_all_lines(ws):
        total += line.count("XMAS") + line.count("SAMX")
    return total


def subset_has_xmas(subset: list[str]) -> bool:
    diagonal = diag(subset, 0, 0, 1, 1)
    antidiagonal = diag(subset, len(subset[0]) - 1, 0, -1, 1)

    return diagonal in ("MAS", "SAM") and antidiagonal in ("MAS", "SAM")


def get_all_xmas_new(ws: list[str]) -> int:
    subsets = get_all_3_by_3(ws)
    return len([ss for ss in subsets if subset_has_xmas(ss)])


if __name__ == '__main__':
    ws = get_word_search("input.txt")
    # ws = ["abcd", "efgh", "ijkl", "mnop"]
    print(get_all_xmas_new(ws))
