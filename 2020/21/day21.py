import re
from dataclasses import dataclass
from functools import reduce
from typing import Set, Iterable


RECIPE_PATTERN = re.compile(r'(.+)\(contains ([a-z, ]+)\)')


@dataclass
class Recipe:
    ingredients: Set[str]
    allergens: Set[str]


def get_recipes(filename: str) -> Iterable[Recipe]:
    with open(filename, 'r') as file:
        for line in file:
            match = RECIPE_PATTERN.match(line.rstrip('\n'))
            ingredients = set(match.group(1).split())
            allergens = set(match.group(2).split(', '))
            yield Recipe(ingredients, allergens)


def part1():
    recipes = list(get_recipes('input.txt'))
    all_allergens = reduce(lambda a, b: a | b, (recipe.allergens for recipe in recipes))
    ingredient_to_allergen = {}
    num_added = 1

    while num_added > 0:
        num_added = 0
        for allergen in all_allergens - set(ingredient_to_allergen.values()):
            ingredients_with_this_allergen = reduce(
                lambda a, b: a & b,
                (recipe.ingredients for recipe in recipes if allergen in recipe.allergens),
            )
            ingredients_with_this_allergen -= set(ingredient_to_allergen.keys())

            if len(ingredients_with_this_allergen) == 1:
                ingredient_to_allergen[next(iter(ingredients_with_this_allergen))] = allergen
                num_added += 1

    print(ingredient_to_allergen)
    allergen_ingredients = set(ingredient_to_allergen.keys())
    count_non_allergens = 0
    for recipe in recipes:
        for ingredient in recipe.ingredients:
            if ingredient not in allergen_ingredients:
                count_non_allergens += 1
    return count_non_allergens


if __name__ == '__main__':
    print(part1())