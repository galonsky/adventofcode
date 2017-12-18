import re

patterns = {
	"set" : re.compile('set ([a-z]) ([a-z]|\-?[0-9]+)'),
	"snd" : re.compile('snd ([a-z]|\-?[0-9]+)'),
	"add" : re.compile('add ([a-z]) ([a-z]|\-?[0-9]+)'),
	"mul" : re.compile('mul ([a-z]) ([a-z]|\-?[0-9]+)'),
	"mod" : re.compile('mod ([a-z]) ([a-z]|\-?[0-9]+)'),
	"rcv" : re.compile('rcv ([a-z]|\-?[0-9]+)'),
	"jgz" : re.compile('jgz ([a-z]|\-?[0-9]+) ([a-z]|\-?[0-9]+)'),}

def get_instr(str):
	for key in patterns:
		match = patterns[key].match(str)
		if match:
			return (key, match)
	raise Exception('wtf')

def value(registers, str):
	if re.match('[a-z]', str):
		return registers.get(str, 0)
	return int(str)


def run_program():
	registers = {}
	last_freq = None
	pc = 0
	with open('day18_input.txt') as file:
		lines = [line for line in file]
		iters = 0
		while pc >= 0 and pc < len(lines):
			pc_incr = 1
			cmd_str = lines[pc].rstrip('\n')
			print(cmd_str)
			instr, match = get_instr(cmd_str)
			if instr == 'set':
				registers[match.groups()[0]] = value(registers, match.groups()[1])
			elif instr == 'add':
				reg = match.groups()[0]
				registers[reg] = registers.get(reg, 0) + value(registers, match.groups()[1])
			elif instr == 'mul':
				reg = match.groups()[0]
				registers[reg] = registers.get(reg, 0) * value(registers, match.groups()[1])
			elif instr == 'mod':
				reg = match.groups()[0]
				registers[reg] = registers.get(reg, 0) % value(registers, match.groups()[1])
			elif instr == 'snd':
				last_freq = value(registers, match.groups()[0])
			elif instr == 'rcv':
				if value(registers, match.groups()[0]) != 0:
					print(last_freq)
					return
			elif instr == 'jgz':
				if value(registers, match.groups()[0]) > 0:
					pc_incr = value(registers, match.groups()[1])

			pc += pc_incr
			iters += 1

run_program()









			