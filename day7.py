import re, statistics

class Node:
	def __init__(self, name, weight, children):
		self.name = name
		self.weight = weight
		self.children = children

	def total_weight(self):
		return self.weight + sum([child.total_weight() for child in self.children])

	def balanced(self):
		if len(self.children) < 2:
			return True

		children_weights = [child.total_weight() for child in self.children]
		return len(set(children_weights)) == 1
		

def parse_tree():
	nodes = {}
	all_children = set()
	with open('day7_input.txt') as file:
		for line in file:
			name, weight_str, children_str = re.search('([a-z]+) \(([0-9]+)\)(?: \-\> (.+))?', line.rstrip('\n')).groups()
			children = children_str.split(', ') if children_str else []
			for child in children:
				all_children.add(child)
			node = Node(name, int(weight_str), children)
			nodes[name] = node
		for name in nodes:
			node = nodes[name]
			node.children = [nodes[child] for child in node.children]

		return nodes['qibuqqg'] # this was the root

		# this found the root
		#print(nodes.keys() - all_children)

def anomaly_helper(node):

	print(['name: {}, weight: {}, total_weight: {}'.format(child.name, child.weight, child.total_weight()) for child in node.children])
	if not node.balanced():
		children_weights = [child.total_weight() for child in node.children]
		mode = statistics.mode(children_weights)
		anomalies = [child for child in node.children if child.total_weight() != mode]

		if all([child.balanced() for child in node.children]):
			# this is the level to correct!
			return (mode - anomalies[0].total_weight()) + anomalies[0].weight

		return anomaly_helper(anomalies[0])

		

def find_anomaly():
	root = parse_tree()
	return anomaly_helper(root)

print(find_anomaly())