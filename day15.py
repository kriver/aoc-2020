#!/usr/bin/env python3

from util import as_int

PUZZLE_INPUT = '0,13,1,16,6,17'


def part1(data: str, iterations: int) -> int:
    numbers = as_int(data.split(','))
    indices = {n: i for i, n in enumerate(numbers[:-1])}
    last = numbers[-1]
    for it in range(len(numbers) - 1, iterations - 1):
        # print('Turn %d, spoke %d' % (it + 1, last))
        if last in indices:
            previous = indices[last]
            indices[last] = it
            last = it - previous
        else:
            indices[last] = it
            last = 0
    return last


if __name__ == "__main__":
    assert 436 == part1('0,3,6', 2020)
    assert 1 == part1('1,3,2', 2020)
    assert 10 == part1('2,1,3', 2020)
    assert 27 == part1('1,2,3', 2020)
    assert 78 == part1('2,3,1', 2020)
    assert 438 == part1('3,2,1', 2020)
    assert 1836 == part1('3,1,2', 2020)

    solution = part1(PUZZLE_INPUT, 2020)
    assert solution == 234
    print('Last number spoken is %d' % solution)

    # assert 175594 == part1('0,3,6', 30000000)
    # assert 2578 == part1('1,3,2', 30000000)
    # assert 3544142 == part1('2,1,3', 30000000)
    # assert 261214 == part1('1,2,3', 30000000)
    # assert 6895259 == part1('2,3,1', 30000000)
    # assert 18 == part1('3,2,1', 30000000)
    # assert 362 == part1('3,1,2', 30000000)

    solution = part1(PUZZLE_INPUT, 30000000)
    assert solution == 8984
    print('Last number spoken is %d' % solution)
