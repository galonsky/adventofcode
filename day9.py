class Garbage:
	def __init__(self):
		self.contents = ''

	def add(self, str):
		self.contents += str

	def __str__(self):
		return '(Garbage: {})'.format(self.contents)

class Group:
	def __init__(self):
		self.contents = []

	def add(self, thing):
		self.contents.append(thing)

	def __str__(self):
		return '(Group: {})'.format(', '.join([str(thing) for thing in self.contents]))

def parse_groups():
	with open('day9_input.txt') as file:
		text = file.read()
		open_group_stack = []
		ignored = False
		current_garbage = None
		first_group = None
		sum_garbage = 0
		for char in text:

			if current_garbage:
				current_garbage.add(char)


			if char == '{' and not current_garbage and not ignored:
				new_group = Group()
				if open_group_stack:
					open_group_stack[-1].add(new_group)
				else:
					first_group = new_group
				open_group_stack.append(new_group)
			elif char == '<' and not current_garbage and not ignored:
				current_garbage = Garbage()
				open_group_stack[-1].add(current_garbage)
				current_garbage.add(char)
			elif char == '>' and current_garbage and not ignored:
				current_garbage = None
			elif char == '}' and not current_garbage and not ignored:
				open_group_stack.pop()

			if current_garbage and not ignored and char != '!' and len(current_garbage.contents) > 1:
				sum_garbage += 1

			if char == '!' and not ignored:
				ignored = True
			else:
				ignored = False
		print(sum_garbage)
		return first_group

def scores_recursive(group, parent_score):
	return parent_score + sum([scores_recursive(child_group, parent_score + 1) for child_group in group.contents if isinstance(child_group, Group)])

def get_score():
	first_group = parse_groups()
	return scores_recursive(first_group, 1)

			
print(get_score())