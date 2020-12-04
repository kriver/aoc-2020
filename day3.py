#!/usr/bin/env python3

from util import *


def down_hill(m, dx, dy):
    num = 0
    dw = len(m[0])
    dh = len(m)
    x, y = 0, 0
    while True:
        if m[y][x] == '#':
            num += 1
        x = (x + dx) % dw
        y = y + dy
        if y >= dh:
            break
    return num


if __name__ == "__main__":
    map = load('day3.txt')

    trees = down_hill(map, 3, 1)
    assert trees == 151
    print("Number of trees: %d" % trees)

    product = 1
    for slope in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
        trees = down_hill(map, *slope)
        product *= trees
    print("Tree product: %d" % product)
