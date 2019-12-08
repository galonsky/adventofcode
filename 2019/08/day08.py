def get_input(filename):
    with open(filename, 'r') as file:
        return file.read()

def get_layers(filename):
    pixels = get_input(filename)
    layers = []
    for i in range(0, len(pixels), 150):
        layers.append(pixels[i:i+150])
    
    least_zeros = min(layers, key=lambda layer: layer.count('0'))
    return least_zeros.count('1') * least_zeros.count('2')

def get_color(layers, idx):
    for layer in layers:
        if layer[idx] != '2':
            return layer[idx]
    return '2'

def print_layers(filename):
    pixels = get_input(filename)
    layers = []
    for i in range(0, len(pixels), 150):
        layers.append(pixels[i:i+150])
    
    for row in range(6):
        for column in range(25):
            idx = row*25 + column
            color = get_color(layers, idx)
            if color == '2':
                print(' ', end='')
            elif color == '1':
                print('*', end='')
            else:
                print(' ', end='')
        print()


print(print_layers('input.txt'))