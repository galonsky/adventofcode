def sublist(nums, start, length):
	if start + length >= len(nums):
		remainder = (start + length) % len(nums)
		return nums[start:] + nums[0:remainder]
	else:
		return nums[start:(start+length)]

def hash():
	#lengths = [83,0,193,1,254,237,187,40,88,27,2,255,149,29,42,100]
	input = '83,0,193,1,254,237,187,40,88,27,2,255,149,29,42,100'
	lengths = []
	for char in input:
		lengths.append(ord(char))
	lengths += [17, 31, 73, 47, 23]
	skip_size = 0
	current_position = 0
	nums = list(range(256))
	for round in range(64):
		for length in lengths:
			reversed = sublist(nums, current_position, length)
			#print('sublist: {}'.format(reversed))
			reversed.reverse()
			#print('reversed: {}'.format(reversed))
			for i, el in enumerate(reversed):
				index = (current_position + i) % len(nums)
				nums[index] = el
			#print('nums: {}'.format(nums))
			current_position = (current_position + length + skip_size) % len(nums)
			skip_size += 1
	#print(nums)
	dense = []
	for block in range(16):
		n = 0
		for i in range(block * 16, block * 16 + 16):
			n ^= nums[i]
		dense.append(n)
	print(dense)
	return bytearray(dense).hex()

#print(sublist([1,2,3,4,5], 3, 2))
print(hash())
