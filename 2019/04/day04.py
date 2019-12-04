def is_valid(num):
    num_str = str(num)
    last_ch = num_str[0]
    double = False
    for i in range(1, len(num_str)):
        ch = num_str[i]
        if ch == last_ch:
            double = True
        if int(ch) < int(last_ch):
            return False
        last_ch = ch
    return double


def get_groups(num_str):
    i = 0
    while i < len(num_str):
        group = ''
        while i < len(num_str) and (len(group) == 0 or num_str[i] == num_str[i-1]):
            group += num_str[i]
            i += 1
        yield group


def has_a_two_group(num_str):
    for group in get_groups(num_str):
        if len(group) == 2:
            return True



def is_valid_pt_2(num):
    num_str = str(num)
    last_ch = num_str[0]
    for i in range(1, len(num_str)):
        ch = num_str[i]
        if int(ch) < int(last_ch):
            return False
        last_ch = ch
    return has_a_two_group(num_str)



def get_num_possible(range_start, range_end):
    count = 0
    for i in range(range_start, range_end + 1):
        print(i)
        if is_valid_pt_2(i):
            count += 1
    return count

print(get_num_possible(264360, 746325))
# print(list(get_groups('112233')))
# print(list(get_groups('123444')))
# print(list(get_groups('111122')))