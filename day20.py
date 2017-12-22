import re
from collections import defaultdict

XP = re.compile('p=\<(\-?[0-9]+),(\-?[0-9]+),(\-?[0-9]+)\>, v=\<(\-?[0-9]+),(\-?[0-9]+),(\-?[0-9]+)\>, a=\<(\-?[0-9]+),(\-?[0-9]+),(\-?[0-9]+)\>')

class Particle:
	def __init__(self, id, position, velocity, acceleration):
		self.id = id
		self.position = position
		self.velocity = velocity
		self.acceleration = acceleration
		
	def distance(self):
		return sum(abs(a) for a in self.position)
		
	def tick(self):
		for i in range(3):
			self.velocity[i] += self.acceleration[i]
			self.position[i] += self.velocity[i]
			
def create_particles():
	particles = {}
	with open('day20_input.txt') as file:
		for id, line in enumerate(file):
			groups = [int(part) for part in XP.match(line.rstrip('\n')).groups()]
			particles[id] = Particle(id, groups[0:3], groups[3:6], groups[6:9])
	return particles
	
def move_particles():
	particles = create_particles()
	for i in range(10000):
		positions = defaultdict(list)
		for id, particle in particles.items():
			particle.tick()
			positions[','.join((str(pos) for pos in particle.position))].append(particle)
		for ps in positions.values():
			if len(ps) >= 2:
				for p in ps:
					del particles[p.id]
		print(i, len(particles))
		#print(min(particles.values(), key=lambda p: p.distance()).id)
	
		
	
move_particles()
