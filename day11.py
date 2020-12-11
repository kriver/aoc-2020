#!/usr/bin/env python3
from typing import List, Tuple, Callable

from util import load

SeatingArea = List[List[int]]
Coord = Tuple[int, int]
CountNeighboursFn = Callable[[Coord, SeatingArea], int]


def parse_seat(c: str) -> int:
    if c == '.':
        return 0
    if c == 'L':
        return 1
    if c == '#':
        return 2
    raise RuntimeError


# adding a border around everything for easy processing
def parse(data: List[str]) -> SeatingArea:
    result = []
    for line in data:
        row = [parse_seat(c) for c in line]
        result.append([0] + row + [0])
    empty_row = [0] * (2 + len(data[0]))
    return [empty_row] + result + [empty_row]


def hash_seating(data: SeatingArea) -> int:
    h = 0
    for row in data:
        for n in row:
            h = h * 3 + n
    return h


def count_seats(data: SeatingArea) -> int:
    num = 0
    for row in data:
        for n in row:
            if n == 2:
                num = num + 1
    return num


def count_neighbours_1(coord: Coord, data: SeatingArea) -> int:
    x, y = coord
    cnt = 0
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            if dx == 0 and dy == 0:
                continue
            cnt += 1 if data[y + dy][x + dx] == 2 else 0
    return cnt


def next_seat(coord: Coord, delta: Coord, data: SeatingArea) -> int:
    x, y = coord
    dx, dy = delta
    while 0 <= x + dx < len(data[0]) and 0 <= y + dy < len(data):
        x += dx
        y += dy
        if data[y][x] != 0:
            return 1 if data[y][x] == 2 else 0
    return 0


def count_neighbours_2(coord: Coord, data: SeatingArea) -> int:
    x, y = coord
    cnt = 0
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            if dx == 0 and dy == 0:
                continue
            cnt += next_seat((x, y), (dx, dy), data)
    return cnt


def evolve(data: SeatingArea, counter: CountNeighboursFn,
           limit: int) -> SeatingArea:
    new = [[0] * len(data[0]) for _ in range(len(data))]
    for y in range(1, len(data) - 1):
        for x in range(1, len(data[0]) - 1):
            if data[y][x] == 0:
                continue
            n = counter((x, y), data)
            if data[y][x] == 1 and n == 0:
                new[y][x] = 2
            elif data[y][x] == 2 and n >= limit:
                new[y][x] = 1
            else:
                new[y][x] = data[y][x]
    return new


def gol_until_steady(data: SeatingArea, counter: CountNeighboursFn,
                     limit: int) -> int:
    previous = {hash_seating(data)}
    num_round = 0
    while True:
        num_round += 1
        # print('Round %d' % num_round)
        data = evolve(data, counter, limit)
        h = hash_seating(data)
        if h in previous:
            break
        previous.add(h)
    return count_seats(data)


if __name__ == "__main__":
    seating = parse(load('day11-test.txt'))
    occupied = gol_until_steady(seating, count_neighbours_1, 4)
    assert occupied == 37
    occupied = gol_until_steady(seating, count_neighbours_2, 5)
    assert occupied == 26

    seating = parse(load('day11.txt'))
    occupied = gol_until_steady(seating, count_neighbours_1, 4)
    assert occupied == 2249
    print('Seat count: %d' % occupied)
    occupied = gol_until_steady(seating, count_neighbours_2, 5)
    assert occupied == 2023
    print('Seat count: %d' % occupied)
