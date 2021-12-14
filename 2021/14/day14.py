from collections import defaultdict
from dataclasses import dataclass
from typing import Optional, Iterator

WINDOW_SIZE = 2


@dataclass
class Node:
    letter: str
    next: "Optional[Node]" = None

    def __iter__(self):
        return NodeIterator(self)


class NodeIterator(Iterator[Node]):

    def __init__(self, root: Node):
        self.cur = Node(letter='', next=root)

    def __next__(self) -> Node:
        if not self.cur.next:
            raise StopIteration
        self.cur = self.cur.next
        return self.cur


    def __iter__(self) -> Iterator[Node]:
        return self


def get_template_and_rules(filename: str) -> tuple[str, dict[str,str]]:
    with open(filename, 'r') as file:
        lines = list(file)
        return (
            lines[0].strip(),
            {
                parts[0]: parts[1] for parts in [line.strip().split(" -> ") for line in lines[2:]]
            }
        )


def process_step(template: str, rules: dict[str, str]) -> str:
    insertions_by_index = {}
    for i in range(len(template) - WINDOW_SIZE + 1):
        substr = template[i:i+WINDOW_SIZE]
        if substr in rules:
            insertions_by_index[i+1] = rules[substr]
    new_template = ""
    for i in range(len(template)):
        if i in insertions_by_index:
            new_template += insertions_by_index[i]
        new_template += template[i]
    return new_template


def process_step_fast(template: Node, rules: dict[str, str]) -> None:
    root = template
    first = root
    second = root.next
    while first and second:
        pattern = first.letter + second.letter
        if pattern in rules:
            new_node = Node(rules[pattern], next=second)
            first.next = new_node
        first = second
        second = second.next


def run_steps(template: Node, rules: dict[str, str], n: int) -> None:
    # for i in range(n):
    #     print(i)
    #     template = process_step(template, rules)
    # return template
    for i in range(n):
        print(i)
        process_step_fast(template, rules)




def get_score(template: str) -> int:
    counts = defaultdict(int)
    for ch in template:
        counts[ch] += 1

    return max(counts.values()) - min(counts.values())


def get_score_ll(template: Node) -> int:
    counts = defaultdict(int)
    for node in template:
        counts[node.letter] += 1

    return max(counts.values()) - min(counts.values())


def string_to_ll(string: str) -> Node:
    root = Node(letter=string[0])
    last = root
    for ch in string[1:]:
        new_node = Node(letter=ch)
        last.next = new_node
        last = new_node
    return root


if __name__ == '__main__':
    template, rules = get_template_and_rules("input.txt")
    # print(template)
    # print(rules)
    root = string_to_ll("HN")
    run_steps(root, rules, 40)
    print(get_score_ll(root))
