def follow_jumps():
	with open('day5_input.txt') as file:
		instructions = [int(line.rstrip('\n')) for line in file]
		i = 0
		count = 0
		while True:
			count += 1
			current_instruction = instructions[i]
			next_index = i + current_instruction
			if next_index < 0 or next_index >= len(instructions):
				return count
			instructions[i] += 1
			i = next_index

def follow_jumps_part_two():
	with open('day5_input.txt') as file:
		instructions = [int(line.rstrip('\n')) for line in file]
		i = 0
		count = 0
		while True:
			count += 1
			current_instruction = instructions[i]
			next_index = i + current_instruction
			if next_index < 0 or next_index >= len(instructions):
				return count
			if current_instruction >= 3:
				instructions[i] -= 1
			else:
				instructions[i] += 1
			i = next_index


print(follow_jumps_part_two())