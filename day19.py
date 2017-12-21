import re

def traverse():
	with open('day19_input.txt') as file:
		map = [list(line.rstrip('\n')) for line in file]
			
		col = map[0].index('|')
		row = 0
		dir = 'down'
		
		letters = ''
		steps = 0
		
		while True:
			
			if row < 0 or col < 0 or row >= len(map) or col >= len(map[row]):
				return steps
			char = map[row][col]
			if char == ' ':
				return steps
				
			steps += 1
			
			if re.match('[A-Z]', char):
				letters += char
				print(letters)
			elif char == '+':
				if dir == 'down' or dir == 'up':
					if (col - 1) >= 0 and map[row][col - 1] != ' ':
						dir = 'left'
					else:
						dir = 'right'
				else:
					if (row - 1) >= 0 and map[row - 1][col] != ' ':
						dir = 'up'
					else:
						dir = 'down'
						
			if dir == 'left':
				col -= 1
			elif dir == 'right':
				col += 1
			elif dir == 'up':
				row -= 1
			else:
				row += 1
				
print(traverse())
