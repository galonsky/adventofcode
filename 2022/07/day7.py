import re
import dataclasses
from typing import Optional, Generator, Set

COMMAND_PATTERN = re.compile(r'\$ (.+)')
FILE_PATTERN = re.compile(r'(\d+) (.+)')
DIR_PATTERN = re.compile(r'dir (.+)')


@dataclasses.dataclass
class FileNode:
    parent: Optional["FileNode"]
    children: dict[str, "FileNode"]
    size: int = 0
    total_size: Optional[int] = None


def get_input(filename: str) -> Generator[str, None, None]:
    with open(filename, 'r') as file:
        for line in file:
            yield line.strip()


def build_file_tree(filename: str) -> FileNode:
    root = FileNode(parent=None, children={})
    wd = root
    line_iter = iter(get_input(filename))
    next_command = next(line_iter, None)
    while next_command:
        match = COMMAND_PATTERN.match(next_command)

        command = match.group(1)
        command_parts = command.split()
        if command_parts[0] == "ls":
            # print(command)
            while output_line := next(line_iter, None):
                if COMMAND_PATTERN.match(output_line):
                    break

                file_match = FILE_PATTERN.match(output_line)
                if file_match:
                    size = int(file_match.group(1))
                    name = file_match.group(2)
                    wd.children[name] = FileNode(parent=wd, children={}, size=size)
                else:
                    dir_match = DIR_PATTERN.match(output_line)
                    name = dir_match.group(1)
                    wd.children[name] = FileNode(parent=wd, children={})
            next_command = output_line
            continue
        elif command_parts[0] == "cd":
            # print(command)
            if command_parts[1] == "/":
                wd = root
            elif command_parts[1] == "..":
                wd = wd.parent
            else:
                wd = wd.children[command_parts[1]]
        else:
            raise Exception("command not supported " + command)
        next_command = next(line_iter, None)

    return root


def populate_total_sizes(node: FileNode) -> None:
    if node.total_size is not None:
        return
    if not node.children:
        node.total_size = node.size
        return

    for c in node.children.values():
        populate_total_sizes(c)

    node.total_size = sum(c.total_size for c in node.children.values())


def get_sum_of_dir_sizes_under_limit(root: FileNode, limit: int) -> int:
    if root.size != 0:
        # don't care about files
        return 0

    total = 0
    if root.total_size <= limit:
        total += root.total_size

    for c in root.children.values():
        total += get_sum_of_dir_sizes_under_limit(c, limit)
    return total


def find_size_to_delete(filename: str) -> int:
    root = build_file_tree(filename)
    populate_total_sizes(root)
    return get_sum_of_dir_sizes_under_limit(root, 100000)


def get_all_dir_sizes(root: FileNode) -> Set[int]:
    if root.size != 0:
        return set()

    return_set = {root.total_size}
    for c in root.children.values():
        return_set |= get_all_dir_sizes(c)
    return return_set


def find_smallest_dir_to_delete(filename: str) -> int:
    root = build_file_tree(filename)
    populate_total_sizes(root)
    capacity = 70000000
    used = root.total_size
    free = capacity - used
    need_to_delete = 30000000 - free

    all_dir_sizes = get_all_dir_sizes(root)
    return min(size for size in all_dir_sizes if size > need_to_delete)


if __name__ == '__main__':
    print(find_smallest_dir_to_delete(filename="input.txt"))