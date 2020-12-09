#!/usr/bin/env python3
from typing import List

from util import load, as_int


def preamble_sums(data: List[int], preamble) -> List[int]:
    sums = []
    for i in range(preamble):
        for j in range(0, i):
            sums.append(data[i] + data[j])
    return sums


def analyse(data: List[int], preamble=25) -> int:
    sums = preamble_sums(data, preamble)
    for i in range(preamble, len(data)):
        if data[i] not in sums:
            return i
        sums.extend([data[i] + data[j] for j in range(i - preamble + 1, i)])
        sums = sums[min(preamble - 1, i - preamble + 1):]
    return -1


def find_weakness(data: List[int], idx: int) -> int:
    needle = data[idx]
    for i in range(idx - 1, 0, -1):
        offset = 0
        summed = data[i]
        while offset == 0 or summed < needle:
            offset += 1
            summed += data[i - offset]
        if summed == needle:
            sub_data = data[i - offset:i]
            return min(sub_data) + max(sub_data)
    return -1


if __name__ == "__main__":
    numbers = as_int(load('day9-test.txt'))
    index = analyse(numbers, 5)
    weakness = find_weakness(numbers, index)
    assert numbers[index] == 127
    assert weakness == 62

    numbers = as_int(load('day9.txt'))
    index = analyse(numbers)
    weakness = find_weakness(numbers, index)
    assert numbers[index] == 41682220
    print('Missing sum is %d, weakness is %d' % (numbers[index], weakness))
