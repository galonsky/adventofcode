def get_input(filename):
    with open(filename, 'r') as file:
        for line in file:
            yield int(line.strip())


def get_fuel_required(mass):
    return mass // 3 - 2


def get_fuel_required_recursive(mass):
    fuel = get_fuel_required(mass)
    if fuel <= 0:
        return 0
    
    return fuel + get_fuel_required_recursive(fuel)


def get_sum_of_weights(filename):
    input = get_input(filename)
    total = 0
    for mass in input:
        total += get_fuel_required(mass)
    return total

def get_sum_of_weights_recursive(filename):
    input = get_input(filename)
    total = 0
    for mass in input:
        total += get_fuel_required_recursive(mass)
    return total
    
print(get_sum_of_weights_recursive('input.txt'))
