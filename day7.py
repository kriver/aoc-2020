#!/usr/bin/env python3
import re
from functools import reduce
from typing import List, Tuple, Dict, Set

from util import load

LINE_REGEX = re.compile(r'^(.*) contain (.*)\.$')
BAG_REGEX = re.compile(r'((?:[0-9]+) )?(.*) bags?')


def parse_bag(bag: str) -> (int, str):
    m = re.match(BAG_REGEX, bag)
    if not m:
        raise RuntimeError
    return int(m.group(1) if m.group(1) else 0), m.group(2)


def parse_line(line: str) -> (str, Tuple[int, str]):
    m = re.match(LINE_REGEX, line)
    if not m:
        raise RuntimeError
    container = parse_bag(m.group(1))
    contents = map(parse_bag, m.group(2).split(', '))
    return container[1], list(contents)


def build_containment_tree(lines: [str]) -> Dict[str, List[str]]:
    tree = {}
    for line in lines:
        container, contents = parse_line(line)
        for num, bag in contents:
            tree.setdefault(bag, []).append(container)
    return tree


def traverse_part_1(tree: Dict[str, List[str]], bag: str) -> Set[str]:
    if bag not in tree:
        return {bag}  # found outer container
    else:
        return set(tree[bag]) | \
               reduce(lambda x, y: x | y,
                      map(lambda b: traverse_part_1(tree, b), tree[bag]))


def part1(file: str) -> int:
    data = load(file)
    t = build_containment_tree(data)
    assert 'shiny gold' in t
    colours = traverse_part_1(t, 'shiny gold')
    # print(colours)
    solution = len(colours)
    print('Part 1 bag count: %d' % solution)
    return solution


def build_container_tree(lines: [str]) -> Dict[str, List[Tuple[int, str]]]:
    tree = {}
    for line in lines:
        container, contents = parse_line(line)
        if contents == [0, 'no other']:
            contents = []
        tree.setdefault(container, []).extend(contents)
    return tree


def traverse_part_2(tree: Dict[str, List[Tuple[int, str]]], bag: str) -> int:
    if bag not in tree:
        return 0
    else:
        return 1 + sum(map(lambda b: b[0] * traverse_part_2(tree, b[1]), tree[bag]))


def part2(file: str) -> int:
    data = load(file)
    t = build_container_tree(data)
    assert 'shiny gold' in t
    # print(t)
    cnt = traverse_part_2(t, 'shiny gold') - 1  # don't count the 'shiny gold'
    print('Part 2 bag count: %d' % cnt)
    return cnt


if __name__ == "__main__":
    c = part1('day7-test.txt')
    assert c == 4

    c = part1('day7.txt')
    assert c == 148

    c = part2('day7-test.txt')
    assert c == 32

    c = part2('day7-test2.txt')
    assert c == 126

    c = part2('day7.txt')
    assert c == 24867
