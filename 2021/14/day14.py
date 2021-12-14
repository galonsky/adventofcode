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


def process_counts(template: str, rules: dict[str, str], n: int) -> dict[str, int]:
    letter_counts = defaultdict(int)
    for ch in template:
        letter_counts[ch] += 1
    pair_counts = count_pairs(template)
    for _ in range(n):
        new_pair_counts = defaultdict(int)
        for pair, count in pair_counts.items():
            rule = rules[pair]
            newpair1 = pair[0] + rule
            newpair2 = rule + pair[1]
            new_pair_counts[newpair1] += count
            new_pair_counts[newpair2] += count
            letter_counts[rule] += count
        pair_counts = new_pair_counts
    return letter_counts


def get_score_from_counts(counts: dict[str, int]) -> int:
    return max(counts.values()) - min(counts.values())


def count_pairs(string: str) -> dict[str, int]:
    pair_counts = defaultdict(int)
    for i in range(len(string) - WINDOW_SIZE + 1):
        pair_counts[string[i:i+WINDOW_SIZE]] += 1
    return pair_counts


if __name__ == '__main__':
    template, rules = get_template_and_rules("input.txt")
    counts = process_counts(template, rules, 40)
    print(get_score_from_counts(counts))
