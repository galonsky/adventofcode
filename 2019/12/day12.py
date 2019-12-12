from dataclasses import dataclass, replace
from itertools import combinations

@dataclass
class Moon:
    x: int
    y: int
    z: int
    v_x: int = 0
    v_y: int = 0
    v_z: int = 0
    
    def apply_gravity(self, other_moon: 'Moon'):
        if self.x < other_moon.x:
            self.v_x += 1
        elif self.x > other_moon.x:
            self.v_x -= 1
        
        if self.y < other_moon.y:
            self.v_y += 1
        elif self.y > other_moon.y:
            self.v_y -= 1
        
        if self.z < other_moon.z:
            self.v_z += 1
        elif self.z > other_moon.z:
            self.v_z -= 1
    
    def apply_velocity(self):
        self.x += self.v_x
        self.y += self.v_y
        self.z += self.v_z
    
    def get_potential_energy(self):
        return abs(self.x) + abs(self.y) + abs(self.z)
    
    def get_kinetic_energy(self):
        return abs(self.v_x) + abs(self.v_y) + abs(self.v_z)
    
    def get_total_energy(self):
        return self.get_potential_energy() * self.get_kinetic_energy()


def iterate_moons(moons, steps):
    for _ in range(steps):
        pairs = combinations(moons, 2)
        for moon_a, moon_b in pairs:
            moon_a.apply_gravity(moon_b)
            moon_b.apply_gravity(moon_a)
        
        for moon in moons:
            moon.apply_velocity()

    total_energy = sum((moon.get_total_energy() for moon in moons))
    print(total_energy)

moons = [
    Moon(x=3, y=-6, z=6),
    Moon(x=10, y=7, z=-9),
    Moon(x=-3, y=-7, z=9),
    Moon(x=-8, y=0, z=4),
]

iterate_moons(moons, 1000)