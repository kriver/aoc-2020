#!/usr/bin/env python3
import math
from typing import List, Tuple

import numpy as np

from util import load, as_int


def arrival_after(time: int, bus: int) -> int:
    after = ((earliest // bus) + 1) * bus
    return after - earliest


def part1(busses: List[int]):
    print('--- Part 1 ---')
    found_time = earliest * earliest
    found_bus = -1
    for bus in busses:
        delta = arrival_after(earliest, bus)
        print('Bus %d will arrive after %d minutes' % (bus, delta))
        if delta < found_time:
            found_time = delta
            found_bus = bus
    print('Earliest bus is %d (%d)' % (found_bus, found_time * found_bus))


# Extended Euclidean Algorithm
# See https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
# Code from https://www.geeksforgeeks.org/euclidean-algorithms-basic-and-extended/
def gcd_extended(a: int, b: int) -> Tuple[int, int, int]:
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = gcd_extended(b % a, a)
    # Update x and y using results of recursive call
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


def part2(busses: str) -> int:
    data_split = busses.split(',')
    with_offsets = zip(data_split[1:], range(len(data_split)))
    bus = [(int(b[0]), 1, 1 + b[1])
           for b in filter(lambda b: b[0] != 'x', with_offsets)]
    bus = sorted(bus, key=lambda e: e[0], reverse=True)
    m0 = 1
    id0 = int(data_split[0])
    while True:
        matches = 0
        for i in range(0, len(bus)):
            id1, m1, offset = bus[i]
            delta = m0 * id0 + offset - m1 * id1
            if delta == 0:
                matches += 1
            elif delta < 0:
                m0 += 1
                break
            else:
                bus[i] = (id1, m1 + math.ceil(delta / id1), offset)
                break
        if matches == len(bus):
            break
        # print(m0*id0)
    print(m0, bus)
    return m0 * id0


# See https://www.reddit.com/r/learnprogramming/comments/7bcw31/least_common_multiple_with_an_offset/
# Note: all bus IDs are prime; hence LCM(a,b) = a*b
def part2b(busses: str, minimum=0) -> int:
    data_split = busses.split(',')
    with_offsets = zip(data_split[1:], range(len(data_split)))
    bus = [(int(b[0]), 1 + b[1])
           for b in filter(lambda b: b[0] != 'x', with_offsets)]
    bus = sorted(bus, key=lambda e: e[0], reverse=True)
    id0, id1 = int(data_split[0]), bus[0][0]
    offset1 = bus[0][1]
    _, a, b = gcd_extended(id0, id1)
    m0 = offset1 * a
    m1 = offset1 * b
    assert m0 * id0 + m1 * id1 == offset1
    m0 *= -1
    assert m0 * id0 + offset1 == m1 * id1
    # start searching at provided minimum
    m0 += math.ceil(((minimum / id0) - m0) / id1) * id1
    while True:
        matches = 0
        # verify other components against multipliers of highest number
        for i in range(1, len(bus)):
            id2, offset2 = bus[i]
            if (m0 * id0 + offset2) % id2 == 0:
                matches += 1
        if matches == len(bus) - 1:
            break
        # jump in steps of id1
        m0 += id1
    print(m0, bus)
    return m0 * id0


# See: https://en.wikipedia.org/wiki/Diophantine_equation
def matrix_magic(a, c) -> int:
    import sys
    sys.path.append('hsnf')
    from hsnf import smith_normal_form

    b, u, v = smith_normal_form(a)
    # A . X = C
    #   B = U . A . V
    # B . V^-1 . X = U . C
    #   Y = V^-1 . X => X = V . Y
    #   D = U . C
    # B . Y = D
    d = np.dot(u, c)
    y = np.linalg.inv(b[:, :b.shape[0]]).dot(d)
    x = v[:, :y.shape[0]].dot(y)
    # actual X = X + n*V[last column]
    m0 = int(x[0, 0])
    delta = v[0, -1]
    return m0 % abs(delta)


def part2c(busses: str) -> int:
    data_split = busses.split(',')
    with_offsets = zip(data_split, range(len(data_split)))
    valid_bus = filter(lambda b: b[0] != 'x', with_offsets)
    bus = [(int(b[0]), b[1]) for b in valid_bus]

    l = len(bus)
    A = np.zeros((l - 1, l), dtype=int)
    C = np.zeros((l - 1, 1), dtype=int)

    id0 = bus[0][0]
    for i in range(1, l):
        id1, offset = bus[i]
        _, a, b = gcd_extended(id0, id1)
        m0 = offset * a
        m1 = offset * b
        assert m0 * id0 + m1 * id1 == offset
        m0 *= -1
        assert m0 * id0 + offset == m1 * id1  # the puzzle definition
        # invariant even when incrementing (m0, m1) with (id1, id0) (once or
        # multiple times)
        assert (m0 + 13 * id1) * id0 + offset == (m1 + 13 * id0) * id1
        # build set of linear equations
        #   m = m01 + id1 . x1 => m - id1 . x1 = m01
        #   m = m02 + id2 . x2 => m - id2 . x2 = m02
        #   ...
        A[i - 1, 0] = 1
        A[i - 1, i] = -id1
        C[i - 1] = m0
    m0 = matrix_magic(A, C)
    return m0 * id0


# see https://en.wikipedia.org/wiki/Chinese_remainder_theorem#Using_the_existence_construction
def part2_crt(busses: str) -> int:
    data_split = busses.split(',')
    with_offsets = zip(data_split, range(len(data_split)))
    valid_bus = filter(lambda b: b[0] != 'x', with_offsets)
    bus = [(int(b[0]), -b[1]) for b in valid_bus]

    n1, x = bus[0]
    n2 = 1
    for b in bus[1:]:
        n1, a1 = n1 * n2, x
        n2, a2 = b
        _, m1, m2 = gcd_extended(n1, n2)
        x = a1 * m2 * n2 + a2 * m1 * n1
        x = x % (n1 * n2)
    return x


if __name__ == "__main__":
    data = load('day13.txt')
    earliest = int(data[0])

    bus_ids = as_int(list(filter(lambda b: b != 'x', data[1].split(','))))
    part1(bus_ids)

    print('--- Part 2 ---')

    # part2 and part2b are TOO SLOW
    # part2c is wrong for the actual puzzle input :-/

    assert part2_crt('17,x,13,19') == 3417
    assert part2_crt('67,7,59,61') == 754018
    assert part2_crt('67,x,7,59,61') == 779210
    assert part2_crt('67,7,x,59,61') == 1261476
    assert part2_crt('7,13,x,x,59,x,31,19') == 1068781
    assert part2_crt('1789,37,47,1889') == 1202161486
    t = part2_crt(data[1])
    assert t == 225850756401039
    print('Earliest time is %d' % t)
