from dataclasses import dataclass, replace
from itertools import combinations
from typing import List
import math

def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

@dataclass
class Moon:
    x: int
    y: int
    z: int
    v_x: int = 0
    v_y: int = 0
    v_z: int = 0

    def apply_gravity_axis(self, other_moon: 'Moon', axis: str):
        v_attr = 'v_' + axis
        if getattr(self, axis) < getattr(other_moon, axis):
            setattr(self, v_attr, getattr(self, v_attr) + 1)
        elif getattr(self, axis) > getattr(other_moon, axis):
            setattr(self, v_attr, getattr(self, v_attr) - 1)
    
    def apply_gravity(self, other_moon: 'Moon'):
        self.apply_gravity_axis(other_moon, 'x')
        self.apply_gravity_axis(other_moon, 'y')
        self.apply_gravity_axis(other_moon, 'z')
    
    def apply_velocity_axis(self, axis: str):
        v_attr = 'v_' + axis
        setattr(self, axis, getattr(self, axis) + getattr(self, v_attr))
    
    def apply_velocity(self):
        self.apply_velocity_axis('x')
        self.apply_velocity_axis('y')
        self.apply_velocity_axis('z')
    
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

def get_loop_for_axis(moons: List[Moon], axis: str, target_positions: List[int], target_vels: List[int]):
    
    i = 1
    while True:
        pairs = combinations(moons, 2)
        for moon_a, moon_b in pairs:
            moon_a.apply_gravity_axis(moon_b, axis)
            moon_b.apply_gravity_axis(moon_a, axis)
        
        for moon in moons:
            moon.apply_velocity_axis(axis)

        new_positions = [getattr(moon, axis) for moon in moons]
        new_vels = [getattr(moon, 'v_' + axis) for moon in moons]
        if new_positions == target_positions and new_vels == target_vels:
            return i
        i += 1

        



def find_steps_until_loop(moons):
    initial_x = [moon.x for moon in moons]
    initial_y = [moon.y for moon in moons]
    initial_z = [moon.z for moon in moons]

    x_loop = get_loop_for_axis(moons, 'x', initial_x, [0]*len(moons))
    y_loop = get_loop_for_axis(moons, 'y', initial_y, [0]*len(moons))
    z_loop = get_loop_for_axis(moons, 'z', initial_z, [0]*len(moons))

    return lcm(x_loop, lcm(y_loop, z_loop))




moons = [
    Moon(x=3, y=-6, z=6),
    Moon(x=10, y=7, z=-9),
    Moon(x=-3, y=-7, z=9),
    Moon(x=-8, y=0, z=4),
]

# iterate_moons(moons, 1000)
print(find_steps_until_loop(moons))