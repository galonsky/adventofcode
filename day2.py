def checksum():
	checksum = 0
	with open('day2_input.txt') as file:
		for line in file:
			nums = [int(num) for num in line.rstrip('\n').split('\t')]
			checksum += (max(nums) - min(nums))
	return checksum

def evenly_divisable():
	checksum = 0
	with open('day2_input.txt') as file:
		for line in file:
			nums = [int(num) for num in line.rstrip('\n').split('\t')]
			desc = sorted(nums, reverse=True)
			for i in range(len(desc)):
				for j in range(i + 1, len(desc)):
					if desc[i] % desc[j] == 0:
						checksum += desc[i] // desc[j]
	return checksum

print(evenly_divisable())