def gen_a(prev):
	return (16807 * prev) % 2147483647

def gen_b(prev):
	return (48271 * prev) % 2147483647

def judge():
	a_prev = 883
	b_prev = 879

	matches = 0
	for i in range(40000000):
		a_prev = gen_a(a_prev)
		b_prev = gen_b(b_prev)
		#print(bin(a_prev & 0xffff), bin(b_prev & 0xffff))
		if ((a_prev & 0xffff) == (b_prev & 0xffff)):
			matches += 1
	print(matches)

judge()