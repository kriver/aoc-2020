#!/usr/bin/env python3
from typing import List, Tuple, Set, Dict, Callable

from day17 import GameOfLife, State
from util import load

Coord = Tuple[int, int]
Grid = Dict[Coord, State]


#       /  \  /  \
#      | NW| | NE|
#   /  \  /  \  /  \
#  | W | | O | | E |
#  \  /  \  /  \  /
#    | SW| | SE|
#    \  /  \  /
#
def flip(lines: List[str]) -> Set[Coord]:
    blacks: Set[Coord] = set()
    for line in lines:
        x, y = 0, 0
        while line:
            if line.startswith('e'):
                x, y = x + 2, y
                line = line[1:]
            elif line.startswith('se'):
                x, y = x + 1, y - 1
                line = line[2:]
            elif line.startswith('sw'):
                x, y = x - 1, y - 1
                line = line[2:]
            elif line.startswith('w'):
                x, y = x - 2, y
                line = line[1:]
            elif line.startswith('nw'):
                x, y = x - 1, y + 1
                line = line[2:]
            elif line.startswith('ne'):
                x, y = x + 1, y + 1
                line = line[2:]
        if (x, y) in blacks:
            blacks.remove((x, y))
        else:
            blacks.add((x, y))
    return blacks


class GameOfLifeHex(GameOfLife):
    def __init__(self, lines: List[str]):
        GameOfLife.__init__(self, [], activate={2}, inactivate={1, 2})
        blacks = flip(lines)
        for coord in blacks:
            self._set_activity(coord, True)

    def new_coord(self, x: int, y: int) -> Coord:
        return x, y

    def update_neighbours(self, coord: Coord, f: Callable[[int], int]):
        cx, cy = coord
        for x, y in [(2, 0), (+1, -1), (-1, -1), (-2, 0), (-1, 1), (1, 1)]:
            c = (cx + x, cy + y)
            self.update_neighbour(c, f)


if __name__ == "__main__":
    data = load('day24-test.txt')
    assert len(flip(data)) == 10
    gol = GameOfLifeHex(data)
    gol.evolve(100)
    assert gol.active() == 2208

    data = load('day24.txt')
    the_blacks = flip(data)
    assert len(the_blacks) == 287
    print('Number of black tiles is %d' % len(the_blacks))

    gol = GameOfLifeHex(data)
    gol.evolve(100)
    assert gol.active() == 3636
    print('Number of black tiles after 100 generations is %d' % gol.active())
