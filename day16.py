import re

SPIN = re.compile('s([0-9]+)')
EXCHANGE = re.compile('x([0-9]+)\/([0-9]+)')
PARTNER = re.compile('p([a-z])\/([a-z])')

def swap_indices(arr, a, b):
	tmp = arr[a]
	arr[a] = arr[b]
	arr[b] = tmp

def process_move(positions, move_str):
	spin_match = SPIN.match(move_str)
	if spin_match:
		spin_val = int(spin_match.groups()[0])
		#print('spin {}'.format(spin_val))
		positions = positions[-spin_val:] + positions[0:-spin_val]
		return positions

	exchange_match = EXCHANGE.match(move_str)
	if exchange_match:
		idx1 = int(exchange_match.groups()[0])
		idx2 = int(exchange_match.groups()[1])
		#print('exchange {} to {}'.format(idx1, idx2))
		swap_indices(positions, idx1, idx2)
		return positions

	partner_match = PARTNER.match(move_str)
	if partner_match:
		letter1 = partner_match.groups()[0]
		letter2 = partner_match.groups()[1]
		#print('partner {} to {}'.format(letter1, letter2))
		swap_indices(positions, positions.index(letter1), positions.index(letter2))
		return positions

	raise Exception('wtf')

def dance():
	positions = []
	for i in range(16):
		positions.append(chr(ord('a') + i))
	original = list(positions)
	print(original)
	permutations = {}

	with open('day16_input.txt') as file:
		move_strs = file.read().split(',')
		# cycled every 180, 1 bil % 180 is 100
		for i in range(100):
		# perm_str = ''.join(positions)
		# print(i, perm_str)
		# if perm_str not in permutations:
		# 	permutations[perm_str] = i
		# else:
		# 	print('at {}, permutation already happened at {}'.format(i, permutations[perm_str]))
			for move_str in move_strs:
				positions = process_move(positions, move_str)
		#print(positions)
		# if positions == original:
		# 	print('found cycle at i={}'.format(i))
			#return
		print(''.join(positions))


dance()