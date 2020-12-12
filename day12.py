#!/usr/bin/env python3
from typing import List, Tuple

from util import load

Coord = Tuple[int, int]

TURN_LEFT = {
    (1, 0): (0, 1),
    (0, 1): (-1, 0),
    (-1, 0): (0, -1),
    (0, -1): (1, 0)
}


def parse(direction: str) -> Tuple[str, int]:
    return direction[0], int(direction[1:])


def turn_1(heading: Coord, value: int) -> Coord:
    steps = value // 90
    for _ in range(steps):
        heading = TURN_LEFT[heading]
    return heading


def move_1(pos: Coord, heading: Coord, directions: List[str]) -> Coord:
    x, y = pos
    for direction in directions:
        action, value = parse(direction)
        if 'N' == action:
            y += value
        elif 'S' == action:
            y -= value
        elif 'E' == action:
            x += value
        elif 'W' == action:
            x -= value
        elif 'L' == action:
            heading = turn_1(heading, value)
        elif 'R' == action:
            heading = turn_1(heading, 360 - value)
        elif 'F' == action:
            x, y = x + heading[0] * value, y + heading[1] * value
        else:
            raise RuntimeError
    return x, y


def turn_2(wp: Coord, value: int) -> Coord:
    # (10,5) -> (-5,10) -> (-10,-5) -> (5,-10)
    if value == 90:
        return -wp[1], wp[0]
    elif value == 180:
        return -wp[0], -wp[1]
    elif value == 270:
        return wp[1], -wp[0]
    else:
        raise RuntimeError


def move_2(pos: Coord, wp: Coord, directions: List[str]) -> Coord:
    for direction in directions:
        action, value = parse(direction)
        if 'N' == action:
            wp = (wp[0], wp[1] + value)
        elif 'S' == action:
            wp = (wp[0], wp[1] - value)
        elif 'E' == action:
            wp = (wp[0] + value, wp[1])
        elif 'W' == action:
            wp = (wp[0] - value, wp[1])
        elif 'L' == action:
            wp = turn_2(wp, value)
        elif 'R' == action:
            wp = turn_2(wp, 360 - value)
        elif 'F' == action:
            pos = pos[0] + wp[0] * value, pos[1] + wp[1] * value
        else:
            raise RuntimeError
    return pos


def manhattan_distance(coord: Coord) -> int:
    return abs(coord[0]) + abs(coord[1])


if __name__ == "__main__":
    data = load('day12-test.txt')
    position = move_1((0, 0), (1, 0), data)
    assert manhattan_distance(position) == 25

    position = move_2((0, 0), (10, 1), data)
    assert manhattan_distance(position) == 286

    data = load('day12.txt')
    position = move_1((0, 0), (1, 0), data)
    assert manhattan_distance(position) == 1319
    print('Manhattan distance: %d' % manhattan_distance(position))

    position = move_2((0, 0), (10, 1), data)
    assert manhattan_distance(position) == 62434
    print('Manhattan distance: %d' % manhattan_distance(position))
