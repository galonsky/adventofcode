import re

BEGIN = re.compile('Begin in state ([A-Z])\.')
DIAG = re.compile('Perform a diagnostic checksum after ([0-9]+) steps\.')
STATE = re.compile('''In state ([A-Z]):
  If the current value is ([01]):
    - Write the value ([01])\.
    - Move one slot to the (right|left)\.
    - Continue with state ([A-Z])\.
  If the current value is ([01]):
    - Write the value ([01])\.
    - Move one slot to the (right|left)\.
    - Continue with state ([A-Z])\.
''')

class Step:
    def __init__(self, write, dir, next):
        self.write = write
        self.dir = dir
        self.next = next

class State:
    def __init__(self, zerostep, onestep):
        self.steps = {
            0: zerostep,
            1: onestep
        }

with open('day25_input.txt') as file:
    lines = [line for line in file]
    start = BEGIN.match(lines[0].rstrip('\n')).groups()[0]
    diag = int(DIAG.match(lines[1].rstrip('\n')).groups()[0])
    states = {}
    tape = {}
    tape_pos = 0
    i = 3
    while i < len(lines):
        state_str = ''.join(lines[i:i+9])
        groups = STATE.match(state_str).groups()
        print(groups)
        states[groups[0]] = State(Step(int(groups[2]), groups[3], groups[4]), Step(int(groups[6]), groups[7], groups[8]))
        #print(state_str)
        i += 10
    print(states)

    state_char = start
    for i in range(diag):
        state = states[state_char]
        cur_tape = tape.get(tape_pos, 0)
        step = state.steps[cur_tape]
        tape[tape_pos] = step.write
        if step.dir == 'right':
            tape_pos += 1
        else:
            tape_pos -= 1
        state_char = step.next

    checksum = 0
    ones = [val for val in tape.values() if val == 1]
    print(len(ones))