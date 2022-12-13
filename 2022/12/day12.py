def get_map(filename: str) -> tuple[list[str], tuple[int, int], tuple[int, int]]:
    rows = []
    start = None
    end = None
    with open(filename, 'r') as file:
        for i, line in enumerate(file):
            stripped = line.strip()
            s_index = stripped.find('S')
            if s_index != -1:
                start = (s_index, i)
            e_index = stripped.find('E')
            if e_index != -1:
                end = (e_index, i)
            rows.append(stripped)
        return rows, start, end


if __name__ == '__main__':
    trail_map, start, end = get_map("sample.txt")
    print(trail_map)
    print(start)
    print(end)