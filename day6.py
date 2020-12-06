#!/usr/bin/env python3
from typing import List

from util import load


def part1(data: List[str]) -> int:
    total = 0
    group = set()
    for line in data:
        if line == '':
            total += len(group)
            group = set()
        else:
            group |= set(line)
    total += len(group)
    return total


def part2(data: List[str]) -> int:
    total = 0
    group = None
    for line in data:
        if line == '':
            total += len(group)
            group = None
        elif group is None:
            group = set(line)
        else:
            group &= set(line)
    total += len(group)
    return total


if __name__ == "__main__":
    lines = load('day6.txt')

    count = part1(lines)
    assert count == 6748
    print('Count = %d' % count)

    count = part2(lines)
    assert count == 3445
    print('Count = %d' % count)
