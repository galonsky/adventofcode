import re
from abc import ABC
from collections import defaultdict
from dataclasses import dataclass
from typing import Callable, Iterable

FOLD_PATTERN = re.compile(r'fold along ([xy])=(\d+)')


class FoldHandler(ABC):
    def get_all_points(
            self,
            paper: dict[tuple[int, int], bool],
            value: int,
    ) -> Iterable[tuple[int, int]]:
        for coord, val in paper.items():
            if val and self.point_should_fold(coord, value):
                yield coord

    def point_should_fold(self, coord: tuple[int, int], value: int) -> bool:
        raise NotImplementedError

    def get_new_coord(self, coord: tuple[int, int], value: int) -> tuple[int, int]:
        raise NotImplementedError

    def fold(self, paper: dict[tuple[int, int], bool], value: int) -> dict[tuple[int, int], bool]:
        new_paper = dict(paper)
        points_below_fold = list(self.get_all_points(paper, value))
        for coord in points_below_fold:
            new_coord = self.get_new_coord(coord, value)
            new_paper[coord] = False
            new_paper[new_coord] = True
        return {
            k: v for k, v in new_paper.items() if v
        }


class YFoldHandler(FoldHandler):

    def point_should_fold(self, coord: tuple[int, int], value: int) -> bool:
        return coord[1] > value

    def get_new_coord(self, coord: tuple[int, int], value: int) -> tuple[int, int]:
        return coord[0], value - (coord[1] - value)


class XFoldHandler(FoldHandler):

    def point_should_fold(self, coord: tuple[int, int], value: int) -> bool:
        return coord[0] > value

    def get_new_coord(self, coord: tuple[int, int], value: int) -> tuple[int, int]:
        return value - (coord[0] - value), coord[1]


HANDLERS_BY_DIMENSION: dict[str, FoldHandler] = {
    "x": XFoldHandler(),
    "y": YFoldHandler(),
}


@dataclass
class Fold:
    dimension: str
    value: int

    def fold(self, paper: dict[tuple[int, int], bool]) -> dict[tuple[int, int], bool]:
        handler = HANDLERS_BY_DIMENSION[self.dimension]
        return handler.fold(paper, self.value)


def get_input(filename: str) -> tuple[dict[tuple[int, int], bool], list[Fold]]:
    paper = defaultdict(lambda: False)
    folds = []
    with open(filename, 'r') as file:
        line_iter = iter(file)
        line = next(line_iter).strip()
        while line:
            parts = line.split(",")
            paper[(int(parts[0]), int(parts[1]))] = True
            line = next(line_iter).strip()

        line = next(line_iter).strip()
        while line:
            match = FOLD_PATTERN.match(line)
            folds.append(Fold(dimension=match.group(1), value=int(match.group(2))))
            try:
                line = next(line_iter).strip()
            except StopIteration:
                break
    return paper, folds


def print_paper(paper: dict[tuple[int, int], bool]) -> None:
    max_y = max(k[1] for k, v in paper.items() if v)
    max_x = max(k[0] for k, v in paper.items() if v)
    for y in range(max_y + 1):
        line = ""
        for x in range(max_x + 1):
            line += "#" if paper.get((x, y)) else "."
        print(line)
    print()


def get_num_dots_after_folds(paper: dict[tuple[int, int], bool], folds: list[Fold]) -> int:
    print_paper(paper)
    for fold in folds:
        paper = fold.fold(paper)
        print_paper(paper)
    return len([v for v in paper.values() if v])


if __name__ == '__main__':
    paper, folds = get_input("input.txt")
    print(paper)
    print(folds)
    print(get_num_dots_after_folds(paper, folds))
    # 928 too high
