#!/usr/bin/env python3
from typing import List, Tuple, Dict, Callable

from day17 import GameOfLife, State
from util import load

Coord = Tuple[int, int]
Grid = Dict[Coord, State]


class GameOfLifeHex(GameOfLife):
    TOKENS: Dict[str, Coord] = {'e': (2, 0), 'se': (+1, -1), 'sw': (-1, -1),
                                'w': (-2, 0), 'nw': (-1, 1), 'ne': (1, 1)}

    def __init__(self, lines: List[str]):
        GameOfLife.__init__(self, [], activate={2}, inactivate={1, 2})
        self._flip(lines)

    def new_coord(self, x: int, y: int) -> Coord:
        return x, y

    def update_neighbours(self, coord: Coord, f: Callable[[int], int]):
        cx, cy = coord
        for x, y in self.TOKENS.values():
            c = (cx + x, cy + y)
            self.update_neighbour(c, f)

    def _flip(self, lines: List[str]):
        for line in lines:
            x, y = 0, 0
            while line:
                for direction, (dx, dy) in self.TOKENS.items():
                    if line.startswith(direction):
                        x, y = x + dx, y + dy
                        line = line[len(direction):]
                        break
            _, active = self._grid.get((x, y), (0, False))
            if active:
                self._set_activity((x, y), False)
            else:
                self._set_activity((x, y), True)


if __name__ == "__main__":
    data = load('day24-test.txt')
    gol = GameOfLifeHex(data)
    assert gol.active() == 10, gol.active()
    gol.evolve(100)
    assert gol.active() == 2208

    data = load('day24.txt')
    gol = GameOfLifeHex(data)
    assert gol.active() == 287
    print('Number of black tiles is %d' % gol.active())
    gol.evolve(100)
    assert gol.active() == 3636
    print('Number of black tiles after 100 generations is %d' % gol.active())
