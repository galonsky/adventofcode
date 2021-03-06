import math

from dataclasses import dataclass
from typing import List, Dict
from collections import defaultdict

@dataclass
class QuantifiedChemical:
    chemical: str
    quantity: int

    @classmethod
    def from_str(cls, string):
        parts = string.split(' ')
        return cls(chemical=parts[1], quantity=int(parts[0]))

@dataclass
class Recipe:
    ingredients: List[QuantifiedChemical]
    result: QuantifiedChemical


def get_recipes(filename):
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(' => ')
            left = parts[0]
            right = parts[1]
            right_chem = QuantifiedChemical.from_str(right)

            left_parts = left.split(', ')
            ingredients = [QuantifiedChemical.from_str(ingredient) for ingredient in left_parts]
            yield Recipe(ingredients=ingredients, result=right_chem)

def get_cost(quantified_chem: QuantifiedChemical, recipes: Dict[str, Recipe], inventory: Dict[str, int]):

    if quantified_chem.chemical == 'ORE':
        return quantified_chem.quantity

    recipe = recipes[quantified_chem.chemical]
    ingredients = recipe.ingredients

    if inventory[quantified_chem.chemical] >= quantified_chem.quantity:
        inventory[quantified_chem.chemical] -= quantified_chem.quantity
        return 0
    
    needed_qty = quantified_chem.quantity - inventory[quantified_chem.chemical]
    inventory[quantified_chem.chemical] = 0
    
    times_to_use_recipe = math.ceil(needed_qty / recipe.result.quantity)
    num_generating = times_to_use_recipe * recipe.result.quantity
    leftover = num_generating - needed_qty
    inventory[recipe.result.chemical] += leftover

    cost_sum = 0
    for ingredient in ingredients:
        needed_qty = ingredient.quantity * times_to_use_recipe
        cost_sum += get_cost(QuantifiedChemical(chemical=ingredient.chemical, quantity=needed_qty), recipes, inventory)
    return cost_sum



def get_cost_of_one_fuel(filename):
    recipes = get_recipes(filename)
    recipes_by_result_chem = {recipe.result.chemical: recipe for recipe in recipes}

    root = recipes_by_result_chem['FUEL']
    assert root.result.quantity == 1

    return get_cost(root.result, recipes_by_result_chem, defaultdict(lambda: 0))

def get_num_fuel_possible(filename, ore=1000000000000):
    recipes = get_recipes(filename)
    recipes_by_result_chem = {recipe.result.chemical: recipe for recipe in recipes}

    root = recipes_by_result_chem['FUEL']
    assert root.result.quantity == 1
    cost_of_one = get_cost(root.result, recipes_by_result_chem, defaultdict(lambda: 0))

    inventory = defaultdict(lambda: 0)
    total_fuel = 0
    while cost_of_one <= ore:
        fuel_to_aim_for = ore // cost_of_one
        total_fuel += fuel_to_aim_for
        cost = get_cost(QuantifiedChemical(chemical='FUEL', quantity=fuel_to_aim_for), recipes_by_result_chem, inventory)
        ore -= cost
    return total_fuel

assert get_cost_of_one_fuel('sample1.txt') == 31
assert get_cost_of_one_fuel('sample2.txt') == 165
assert get_cost_of_one_fuel('sample3.txt') == 13312
assert get_cost_of_one_fuel('sample4.txt') == 180697
assert get_cost_of_one_fuel('sample5.txt') == 2210736
assert get_cost_of_one_fuel('input.txt') == 248794

assert get_num_fuel_possible('sample3.txt') == 82892753
assert get_num_fuel_possible('sample4.txt') == 5586022
assert get_num_fuel_possible('sample5.txt') == 460664
assert get_num_fuel_possible('input.txt') == 4906796