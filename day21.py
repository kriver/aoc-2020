#!/usr/bin/env python3
import re
from typing import List, Dict, Tuple, Set

from util import load

LINE_RE = r'(.*) \(contains (.*)\)'

Food = List[Set[str]]
Allergens = Dict[str, List[int]]


def parse(lines: List[str]) -> Tuple[Food, Allergens, Set[str]]:
    food = []
    allergens_map: Allergens = {}
    all_ingredients = set()
    i = 0
    for line in lines:
        m = re.match(LINE_RE, line)
        if not m:
            raise RuntimeError
        ingredients = [s.strip() for s in m.group(1).split(' ')]
        food.append(set(ingredients))
        allergens = [s.strip() for s in m.group(2).split(',')]
        for a in allergens:
            allergens_map.setdefault(a, [])
            allergens_map[a].append(i)
        all_ingredients |= set(ingredients)
        i += 1
    return food, allergens_map, all_ingredients


def unsafe_ingredients(food: Food, allergens: Allergens) -> Set[str]:
    unsafe: Set[str] = set()
    for a, indices in allergens.items():
        foods = [food[i] for i in indices]
        unsafes = set.intersection(*foods)
        unsafe |= unsafes
    return unsafe


def count_safe(food: Food, safe: Set[str]) -> int:
    count = 0
    for f in food:
        count += len(f & safe)
    return count


def update_food(food: Food, to_be_removed: Set[str]) -> Food:
    for i in range(len(food)):
        food[i] = food[i] - to_be_removed
    return food


def map_unsafe(food: Food, safe_ingredients: Set[str], allergens: Allergens) \
        -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    # remove safe ingredients
    food = update_food(food, safe_ingredients)
    # create mapping
    while True:
        for a, indices in allergens.items():
            foods = [food[i] for i in indices]
            unsafe = set.intersection(*foods)
            if len(unsafe) == 1:
                food = update_food(food, unsafe)
                mapping[a] = unsafe.pop()
        for a in mapping.keys():
            if a in allergens:
                del allergens[a]
        if not allergens:
            break
    return mapping


def to_alpha_list(mapping: Dict[str, str]) -> str:
    return ','.join(mapping[allergen] for allergen in sorted(mapping.keys()))


if __name__ == "__main__":
    the_food, the_allergens, the_ingredients = parse(load('day21-test.txt'))
    the_unsafe = unsafe_ingredients(the_food, the_allergens)
    the_safe = the_ingredients - the_unsafe
    assert count_safe(the_food, the_safe) == 5
    the_mapping = map_unsafe(the_food, the_safe, the_allergens)
    assert to_alpha_list(the_mapping) == 'mxmxvkd,sqjhc,fvjkl'

    the_food, the_allergens, the_ingredients = parse(load('day21.txt'))
    the_unsafe = unsafe_ingredients(the_food, the_allergens)
    the_safe = the_ingredients - the_unsafe
    the_count = count_safe(the_food, the_safe)
    assert the_count == 2517
    print('Number of use of safe ingredients is %d' % the_count)
    the_mapping = map_unsafe(the_food, the_safe, the_allergens)
    the_dangerous = to_alpha_list(the_mapping)
    assert the_dangerous == 'rhvbn,mmcpg,kjf,fvk,lbmt,jgtb,hcbdb,zrb'
    print('Dangerous ingredients: %s' % the_dangerous)
