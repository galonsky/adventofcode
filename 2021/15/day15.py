from collections import defaultdict


def get_map(filename: str) -> list[list[int]]:
    rows = []
    with open(filename, 'r') as file:
        for line in file:
            rows.append([int(ch) for ch in line.strip()])
    return rows


def find_lowest_total_risk(cavern_map: list[list[int]]) -> int:
    dest_y = len(cavern_map) - 1
    dest_x = len(cavern_map[dest_y]) - 1

    dist = {}
    prev = {}

    q = set()


    for y, row in enumerate(cavern_map):
        for x, risk in enumerate(row):
            dist[(x, y)] = float("inf")
            q.add((x, y))

    dist[(0, 0)] = 0
    while q:
        print(len(q))
        u = min(q, key=lambda coord: dist[coord])
        q.remove(u)

        def is_neighbor(coord: tuple[int, int]) -> bool:
            return (
                u == (coord[0] + 1, coord[1])
                or u == (coord[0], coord[1] + 1)
                or u == (coord[0] - 1, coord[1])
                or u == (coord[0], coord[1] - 1)
            )

        if u == (dest_x, dest_y):
            return dist[(dest_x, dest_y)]

        for v in (
            coord for coord in q if is_neighbor(coord)
        ):
            alt = dist[u] + cavern_map[v[1]][v[0]]
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u

    return dist[(dest_x, dest_y)]





if __name__ == '__main__':
    cavern_map = get_map("input.txt")
    # print(cavern_map)
    print(find_lowest_total_risk(cavern_map))