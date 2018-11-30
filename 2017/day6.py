def get_number_of_redistributions():
    with open('day6_input.txt') as file:
        initial_configuration = [int(num) for num in file.read().rstrip('\n').split('\t')]
        arr = initial_configuration
        previous_configs = set()
        config_dict = {}
        previous_configs.add(serialize(initial_configuration))
        config_dict[serialize(initial_configuration)] = 0
        num = 0
        while True:
            num += 1
            arr = redistribute(arr)
            if serialize(arr) in previous_configs:
                # (part one)
                # return num
                return num - config_dict[serialize(arr)]
            previous_configs.add(serialize(arr))
            config_dict[serialize(arr)] = num


def serialize(arr):
    return '-'.join([str(el) for el in arr])


def redistribute(initial):
    arr = list(initial)
    start_index = 0
    max = 0
    for i, num in enumerate(arr):
        if num > max:
            start_index = i
            max = num
    # print('start_index: {}, max: {}'.format(start_index, max))
    arr[start_index] = 0
    for i in range(1, max + 1):
        index = (start_index + i) % len(arr)
        arr[index] += 1
    return arr


print(get_number_of_redistributions())
