from collections import defaultdict


def get_lists(filename: str) -> tuple[list[int], list[int]]:
    l1 = []
    l2 = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.split()
            l1.append(int(parts[0]))
            l2.append(int(parts[1]))
    return l1, l2


def find_total_distance(l1: list[int], l2: list[int]) -> int:
    l1_sorted = sorted(l1)
    l2_sorted = sorted(l2)

    distance = 0
    for i in range(len(l1)):
        distance += abs(l1_sorted[i] - l2_sorted[i])
    return distance


def find_similarity_score(l1: list[int], l2: list[int]) -> int:
    l2_counts = defaultdict(int)
    for n in l2:
        l2_counts[n] += 1

    return sum(n * l2_counts.get(n, 0) for n in l1)


if __name__ == '__main__':
    lists = get_lists("input.txt")
    # print(find_total_distance(*lists))
    print(find_similarity_score(*lists))