from typing import Generator, Iterable


def get_reports(filename: str) -> Generator[list[int], None, None]:
    with open(filename, 'r') as file:
        for line in file:
            parts = line.split()
            yield [int(part) for part in parts]


def is_report_safe(report: list[int]) -> bool:
    differences = [report[i] - report[i-1] for i in range(1, len(report))]
    return all(
        1 <= abs(differences[i]) <= 3
        and ((differences[i] > 0) == (differences[0] > 0))
        for i in range(len(differences))
    )


def get_num_safe_reports(reports: Iterable[list[int]]) -> int:
    return len([report for report in reports if is_report_safe(report)])


if __name__ == '__main__':
    reports = get_reports("input.txt")
    print(get_num_safe_reports(reports))