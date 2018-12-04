import re
from collections import defaultdict

SHIFT_PATTERN = re.compile(r'\[\d+-\d+-\d+ \d+:(\d+)\] Guard #(\d+) begins shift')
SLEEP_PATTERN = re.compile(r'\[\d+-\d+-\d+ \d+:(\d+)\] falls asleep')
WAKE_PATTERN = re.compile(r'\[\d+-\d+-\d+ \d+:(\d+)\] wakes up')


def get_lines(filename):
    with open(filename) as file:
        for line in file:
            yield line.rstrip('\n')


def max_key_by_value(dict):
    max_key = None
    max_value = -1
    for key, value in dict.items():
        if value > max_value:
            max_key = key
            max_value = value
    return max_key


def get_sleepiest_guard_and_minute(filename):
    lines = sorted(list(get_lines(filename)))
    sleep_minutes_by_id = defaultdict(int)
    minute_slept_freqs_by_id = defaultdict(lambda: defaultdict(int))
    i = 0
    while i < len(lines):
        shift = lines[i]
        shift_match = SHIFT_PATTERN.match(shift)
        id = int(shift_match.group(2))

        i += 1
        while i < len(lines) and (not SHIFT_PATTERN.match(lines[i])):
            sleep_match = SLEEP_PATTERN.match(lines[i])
            sleep_minute = int(sleep_match.group(1))
            i += 1
            wake_match = WAKE_PATTERN.match(lines[i])
            wake_minute = int(wake_match.group(1))
            sleep_minutes_by_id[id] += (wake_minute - sleep_minute)
            i += 1
            for minute in range(sleep_minute, wake_minute):
                minute_slept_freqs_by_id[id][minute] += 1
    #part 1
    #sleepiest_id = max_key_by_value(sleep_minutes_by_id)
    #return sleepiest_id, max_key_by_value(minute_slept_freqs_by_id[sleepiest_id])

    #part 2
    flattened_freqs = {}
    for id, freq_dict in minute_slept_freqs_by_id.items():
        for minute, freq in freq_dict.items():
            key = '{},{}'.format(id, minute)
            flattened_freqs[key] = freq
    return max_key_by_value(flattened_freqs)


print(get_sleepiest_guard_and_minute('day4_input.txt'))
