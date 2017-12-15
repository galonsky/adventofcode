from day10 import hash

def find_num_used():
	count = 0
	rows = []
	for row in range(128):
		input = 'hfdlxzhv-{}'.format(row)
		hash_hex = hash(input)
		row_str = ''
		for start in range(0, 32, 2):
			binary = bin(bytearray.fromhex(hash_hex[start:start+2])[0]).lstrip('0b')
			row_str += binary.rjust(8, '0')
			#print(hash_hex[start:start+2], binary)
			count += binary.count('1')
		rows.append(list(row_str))

	region_num = 2
	for row in range(128):
		for col in range(128):
			if rows[row][col] == '1':
				flood_fill(rows, row, col, region_num)
				region_num += 1



	# print(rows)
	# print([len(row) for row in rows])
	# return count

	return region_num - 2

def flood_fill(data, row, col, region_num):
	if row < 0 or row >= len(data) or col < 0 or col >= len(data):
		return
	if data[row][col] == '0':
		return
	if data[row][col] == region_num:
		return
	if data[row][col] == '1':
		data[row][col] = region_num

	flood_fill(data, row + 1, col, region_num)
	flood_fill(data, row - 1, col, region_num)
	flood_fill(data, row, col + 1, region_num)
	flood_fill(data, row, col - 1, region_num)

print(find_num_used())