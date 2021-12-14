from collections import defaultdict

WINDOW_SIZE = 2


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


def run_steps(template: str, rules: dict[str, str], n: int) -> str:
    for _ in range(n):
        template = process_step(template, rules)
    return template


def get_score(template: str) -> int:
    counts = defaultdict(int)
    for ch in template:
        counts[ch] += 1

    return max(counts.values()) - min(counts.values())


if __name__ == '__main__':
    template, rules = get_template_and_rules("input.txt")
    # print(template)
    # print(rules)
    new_template = run_steps(template, rules, 10)
    print(get_score(new_template))