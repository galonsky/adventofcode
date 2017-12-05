import math

def spiral_distance(n):
	root = math.ceil(math.sqrt(n))
	ring = root // 2
	side_len = ring * 2 + 1
	ring_index = n - (max(side_len - 2, 0) ** 2 + 1)
	first_axis = max(ring - 1, 0)
	dist_from_axis = abs((ring_index % max(side_len - 1, 1)) - first_axis)
	print('N: {}, Ring: {}, Side length: {}, Ring Index :{}, Dist from axis: {}'
		.format(n, ring, side_len, ring_index, dist_from_axis))
	return ring + dist_from_axis

print(spiral_distance(312051))