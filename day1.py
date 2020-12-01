#!/usr/bin/env python3

from util import *

GOAL = 2020


def part1(data, m):
    for e1 in data:
        if e1 + m > GOAL:
            continue
        for e2 in data:
            if e1 + e2 == GOAL:
                return e1, e2
    return 0, 0


def part2(data, m):
    for e1 in data:
        if e1 + 2 * m >= GOAL:
            continue
        for e2 in data:
            if e1 + e2 + m > GOAL:
                continue
            for e3 in data:
                if e1 + e2 + e3 == GOAL:
                    return e1, e2, e3
    return 0, 0, 0


if __name__ == "__main__":
    expenses = as_int(load('day1.txt'))
    minimum = min(expenses)

    entry1, entry2 = part1(expenses, minimum)
    assert (entry1, entry2) == (1491, 529)
    print("Part 1: %d x %d = %d" % (entry1, entry2, entry1 * entry2))

    entry1, entry2, entry3 = part2(expenses, minimum)
    assert (entry1, entry2, entry3) == (222, 843, 955)
    print("Part 2: %d x %d x %d = %d" % (entry1, entry2, entry3, entry1 * entry2 * entry3))
