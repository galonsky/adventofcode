import re
import collections
import concurrent.futures

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


class Program:
	
	def __init__(self, instrs, pid, in_queue, out_queue):
		self.instrs = instrs
		self.pid = pid
		self.in_queue = in_queue
		self.out_queue = out_queue
		self.registers = {
			'p': pid
		}
		self.pc = 0
		self.total_sent = 0

	def run_program(self):
		sent = False
		last_freq = None
		
			
		iters = 0
		times_sent = 0
		while self.pc >= 0 and self.pc < len(self.instrs):
			pc_incr = 1
			cmd_str = self.instrs[self.pc]
			#print(pid, cmd_str)
			instr, match = get_instr(cmd_str)
			if instr == 'set':
				self.registers[match.groups()[0]] = value(self.registers, match.groups()[1])
			elif instr == 'add':
				reg = match.groups()[0]
				self.registers[reg] = self.registers.get(reg, 0) + value(self.registers, match.groups()[1])
			elif instr == 'mul':
				reg = match.groups()[0]
				self.registers[reg] = self.registers.get(reg, 0) * value(self.registers, match.groups()[1])
			elif instr == 'mod':
				reg = match.groups()[0]
				self.registers[reg] = self.registers.get(reg, 0) % value(self.registers, match.groups()[1])
			elif instr == 'snd':
				last_freq = value(self.registers, match.groups()[0])
				self.total_sent += 1
				print('{} sending {}'.format(self.pid, last_freq))
				self.out_queue.appendleft(last_freq)
				sent = True
			elif instr == 'rcv':
				if len(self.in_queue) == 0:
					if not sent:
						return 'blocked'
					return 'kinda'
				
				reg = match.groups()[0]
				val = self.in_queue.pop()
				self.registers[reg] = val
				print('{} receiving {}'.format(self.pid, val))
			elif instr == 'jgz':
				if value(self.registers, match.groups()[0]) > 0:
					pc_incr = value(self.registers, match.groups()[1])

			self.pc += pc_incr
			iters += 1
		return 'exit'
		
with open('day18_input.txt') as file:
	instrs = [line.rstrip('\n') for line in file]
	q0 = collections.deque()
	q1 = collections.deque()
	prg0 = Program(instrs, 0, q0, q1)
	prg1 = Program(instrs, 1, q1, q0)
	
	ret0 = prg0.run_program()
	ret1 = prg1.run_program()
	
	while not (ret1 == 'blocked' and ret0 == 'blocked'):
		ret0 = prg0.run_program()
		ret1 = prg1.run_program()
	print('both vloxked')

	print(prg1.total_sent)
