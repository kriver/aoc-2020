#!/usr/bin/env python3
from typing import List

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


def part2(busses: str) -> int:
    data__split = busses.split(',')
    with_offsets = zip(data__split, range(len(data__split)))
    bus_ids = [(int(b[0]), b[1])
               for b in filter(lambda b: b[0] != 'x', with_offsets)]

    return 0


if __name__ == "__main__":
    data = load('day13.txt')
    earliest = int(data[0])

    bus_ids = as_int(list(filter(lambda b: b != 'x', data[1].split(','))))
    part1(bus_ids)

    print('--- Part 2 ---')
    assert part2('17,x,13,19') == 3417
    assert part2('67,7,59,61') == 754018
    assert part2('67,x,7,59,61') == 779210
    assert part2('67,7,x,59,61') == 1261476
    assert part2('7,13,x,x,59,x,31,19') == 1068781
    assert part2('1789,37,47,1889') == 1202161486
    time = part2(data[1])
    # assert time ==
    print('Earliest time is %d', time)
