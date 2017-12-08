import re

def should_process_instruction(cur_val, operator, operand):
	if operator == '==':
		return cur_val == operand
	elif operator == '!=':
		return cur_val != operand
	elif operator == '>':
		return cur_val > operand
	elif operator == '<':
		return cur_val < operand
	elif operator == '<=':
		return cur_val <= operand
	elif operator == '>=':
		return cur_val >= operand
	else:
		raise Exception('unsupported operator ' + operator)

def process_instructions():
	registers = {}
	with open('day8_input.txt') as file:
		max = 0
		for line in file:
			groups = re.search('([a-z]+) (inc|dec) (\-?[0-9]+) if ([a-z]+) (.+) (\-?[0-9]+)', line.rstrip('\n')).groups()
			reg_to_check = groups[3]
			operator = groups[4]
			operand = int(groups[5])
			cur_val = registers.get(reg_to_check, 0)
			if should_process_instruction(cur_val, operator, operand):
				if groups[1] == 'inc':
					registers[groups[0]] = registers.get(groups[0], 0) + int(groups[2])
				else:
					registers[groups[0]] = registers.get(groups[0], 0) - int(groups[2])
				if registers[groups[0]] > max:
					max = registers[groups[0]]
		#return max(registers.values())
		return max

print(process_instructions())
