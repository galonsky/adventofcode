class Node:
	def __init__(self, data):
		self.next = None
		self.data = data


def spinlock():
	buffer = Node(0)
	buffer.next = buffer
	head = buffer
	num_steps = 329
	current_position = 0
	last_second = -1
	count_same = 0
	for i in range(1, 50000000):
		if i % 100000 == 0:
			print(i)

		for j in range(num_steps):
			buffer = buffer.next

		old_head = buffer
		new_node = Node(i)
		new_node.next = old_head.next
		old_head.next = new_node
		buffer = new_node
		#idx_after_steps = (current_position + num_steps) % len(buffer)
		#buffer.insert(idx_after_steps + 1, i)
		#current_position = idx_after_steps + 1
		#print(i, current_position)
		#print(i)
		#print(i, buffer[0:3])
		# if buffer[1] != last_second:
			
		# 	count_same = 0
		# 	last_second = buffer[1]
		# 	print('Second is {} at {}'.format(last_second, i))
		# else:
		# 	count_same += 1

	# zero_idx = buffer.index(0)
	# print(buffer[zero_idx + 1])
	#print(buffer.next.data)
	# find 0, print next



spinlock()