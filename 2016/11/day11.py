import json
import operator
from collections import deque
from copy import deepcopy
from dataclasses import dataclass
from functools import reduce
from itertools import chain, combinations
from typing import List, Set, Tuple, Optional, Iterable

# INITIAL = [
#     {"HM", "LM"},
#     {"HG"},
#     {"LG"},
#     set(),
# ]

# INITIAL = [
#     {"OG", "TG", "TM", "PG", "RG", "RM", "CG", "CM"},
#     {"OM", "PM"},
#     set(),
#     set(),
# ]

INITIAL = [
    {"OG", "TG", "TM", "PG", "RG", "RM", "CG", "CM", "EG", "EM", "DG", "DM"},
    {"OM", "PM"},
    set(),
    set(),
]

num_floors = len(INITIAL)
num_objects = sum(len(floor) for floor in INITIAL)


def serialize_state(state: List[Set[str]], elevator: int) -> str:
    return json.dumps({
        "elevator": elevator,
        "floors": [
            sorted(item[1:] for item in floor) for floor in state
        ]
    })


def transform_state(state: List[Set[str]], objects: Tuple[str, ...], from_floor: int, to_floor: int) -> List[Set[str]]:
    new_state = deepcopy(state)
    new_state[from_floor] -= set(objects)
    new_state[to_floor] |= set(objects)
    return new_state


def is_valid(state: List[Set[str]]) -> bool:
    for floor in state:
        chips = {obj for obj in floor if obj.endswith("M")}
        for chip in chips:
            element = chip[0]
            corresponding_generator = element + "G"
            if corresponding_generator not in floor:
                if any(obj for obj in floor if obj.endswith("G")):
                    return False
    return True


def print_state(state: List[Set[str]], elevator: int):
    objects_in_order = sorted(reduce(operator.or_, INITIAL))

    for i in reversed(range(len(state))):
        floor = state[i]
        line = ""
        line += f"F{i+1} "
        if i == elevator:
            line += "E"
        else:
            line += "."
        line += "  "

        for c, obj in enumerate(objects_in_order):
            if obj in floor:
                line += obj
            else:
                line += ". "
            line += " "
        print(line)
    print()


@dataclass
class Attempt:
    state: List[Set[str]]
    elevator: int
    num_steps: int = 0


visited = {}
queue: deque[Attempt] = deque()


def get_possible_moves(going_up: bool, on_floor: Set[str]) -> Iterable[Tuple[str, ...]]:
    one_moves = list(combinations(on_floor, 1))
    two_moves = list(combinations(on_floor, 2))
    if going_up:
        return two_moves or one_moves
    else:
        return one_moves or two_moves



def run_elevator(attempt: Attempt) -> Optional[int]:
    state = attempt.state
    elevator = attempt.elevator
    num_steps = attempt.num_steps
    # print_state(state, elevator)
    serialized = serialize_state(state, elevator)
    if visited.get(serialized, float("inf")) < num_steps:
        return

    on_floor = state[elevator]
    if not on_floor:
        raise Exception('empty floor?')
    if len(on_floor) == num_objects and elevator == num_floors - 1:
        print(f"Done! {num_steps}")
        return num_steps

    new_floors = filter(lambda i: 0 <= i < num_floors, (elevator - 1, elevator + 1))
    floor_and_states: List[Tuple[int, List[Set[str]]]] = []

    for new_floor in new_floors:
        going_up = new_floor > elevator
        going_down = not going_up

        if going_down and not any(state[0:elevator]):
            continue

        possible_moves = get_possible_moves(going_up, on_floor)
        for objects_to_move in possible_moves:
            new_state = transform_state(state, objects_to_move, elevator, new_floor)
            serialized = serialize_state(new_state, new_floor)
            if is_valid(new_state) and num_steps + 1 < visited.get(serialized, float("inf")):
                visited[serialized] = num_steps + 1
                floor_and_states.append((new_floor, new_state))

    for (f, s) in floor_and_states:
        att = Attempt(s, f, num_steps + 1)
        queue.append(att)


if __name__ == "__main__":
    queue.append(Attempt(INITIAL, 0))
    while queue:
        print(f"Q length {len(queue)}")
        print(f"Visited length {len(visited)}")
        att = queue.popleft()
        res = run_elevator(att)
        if res is not None:
            exit(0)
