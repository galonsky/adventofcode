def xy_key(x, y):
	return '{},{}'.format(x,y)
	
def import_infections():
	infections = {}
	with open('day22_input.txt') as file:
		lines = [line.rstrip('\n') for line in file]
		half = len(lines) // 2
		for row in range(len(lines)):
			for col in range(len(lines)):
				if lines[row][col] == '#':
					x = col - half
					y = half - row
					key = xy_key(x, y)
					infections[key] = 'i'
	return infections

infections = import_infections()
x = 0
y = 0
directions = ['up', 'right', 'down', 'left']
dir_index = 0
infections_caused = 0

for iter in range(10000000):
	key = xy_key(x, y)
	state = infections.get(key, 'c')
	if state == 'i':
		infections[key] = 'f'
		dir_index += 1
	elif state == 'c':
		infections[key] = 'w'
		dir_index -= 1
	elif state == 'w':
		infections[key] = 'i'
		infections_caused += 1
	elif state == 'f':
		del infections[key]
		dir_index += 2
		
	direction = directions[dir_index % 4]
	if direction == 'up':
		y += 1
	elif direction == 'right':
		x += 1
	elif direction == 'down':
		y -= 1
	elif direction == 'left':
		x -= 1
		
print(infections_caused)
