def get(n, k):
	up = (k // n) % 2 == 0

	if up:
		return k % n
	else:
		return n - k % n

def find_penalty():
	with open('day13_input.txt') as file:
		scanners = {}
		for line in file:
			parts = line.rstrip('\n').split(': ')
			depth = int(parts[0])
			rng = int(parts[1])
			scanners[depth] = rng
		# penalty = 0
		# for depth in range(max(scanners.keys()) + 1):
		# 	if depth in scanners:
		# 		scanner_pos = get(scanners[depth] - 1, max(depth, 0))
		# 		print('Depth: {}, Scanner Pos: {}'.format(depth, scanner_pos))
		# 		if scanner_pos == 0:
		# 			penalty += depth * scanners[depth]
		# return penalty
		i = 0
		while True:
			print(i)
			if not would_get_caught(scanners, i):
				return i
			i += 1

def would_get_caught(scanners, start_time):
	for depth in range(max(scanners.keys()) + 1):
		if depth in scanners:
			scanner_pos = get(scanners[depth] - 1, depth + start_time)
			if scanner_pos == 0:
				return True
	return False

print(find_penalty())

