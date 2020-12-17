#!/usr/bin/env python3
from typing import Tuple, List, Dict, Callable, Generic, TypeVar

from util import load

G = TypeVar('G')
C = TypeVar('C')

State = Tuple[int, bool]

Coord3D = Tuple[int, int, int]
Grid3D = Dict[Coord3D, State]

Coord4D = Tuple[int, int, int, int]
Grid4D = Dict[Coord4D, State]


class GameOfLife(Generic[G, C]):
    def __init__(self, lines: List[str]):
        self._grid: G = {}
        y = 0
        for line in lines:
            for x, c in enumerate(line):
                if c == '#':
                    self._set_activity(self.new_coord(x, y), True)
            y += 1

    @staticmethod
    def _inc(a: int) -> int:
        return a + 1

    @staticmethod
    def _dec(a: int) -> int:
        return a - 1 if a > 0 else 0

    def new_coord(self, x: int, y: int) -> C:
        raise RuntimeError

    def update_neighbours(self, coord: C, f: Callable[[int], int]):
        raise RuntimeError

    def update_neighbour(self, coord: C, f: Callable[[int], int]):
        if coord not in self._grid:
            self._grid[coord] = (0, False)
        neighbours, state = self._grid[coord]
        self._grid[coord] = (f(neighbours), state)

    def _set_activity(self, coord: C, state: bool):
        if coord not in self._grid:
            self._grid[coord] = (0, state)
            self.update_neighbours(coord, GameOfLife._inc)
        else:
            neighbours, prev_state = self._grid[coord]
            if prev_state != state:
                self.update_neighbours(coord,
                                       GameOfLife._inc if state
                                       else GameOfLife._dec)
                self._grid[coord] = (neighbours, state)

    def _evolve_1(self):
        current = self._grid.copy()
        for coord, state in current.items():
            neighbours, active = state
            if active and neighbours not in {2, 3}:
                self._set_activity(coord, False)
            elif not active and neighbours == 3:
                self._set_activity(coord, True)

    def evolve(self, generations: int):
        for generation in range(generations):
            self._evolve_1()
            print('Generation %d has %d active cubes'
                  % (generation + 1, self.active()))

    def active(self) -> int:
        return len([s for n, s in self._grid.values() if s])


class GameOfLife3D(GameOfLife[Grid3D, Coord3D]):
    def __init__(self, lines: List[str]):
        GameOfLife.__init__(self, lines)

    def new_coord(self, x: int, y: int) -> Coord3D:
        return x, y, 0

    def update_neighbours(self, coord: Coord3D, f: Callable[[int], int]):
        cx, cy, cz = coord
        for x in range(-1, 2):
            for y in range(-1, 2):
                for z in range(-1, 2):
                    if x == y == z == 0:
                        continue
                    c = (cx + x, cy + y, cz + z)
                    self.update_neighbour(c, f)


class GameOfLife4D(GameOfLife[Grid4D, Coord4D]):
    def __init__(self, lines: List[str]):
        GameOfLife.__init__(self, lines)

    def new_coord(self, x: int, y: int) -> Coord4D:
        return x, y, 0, 0

    def update_neighbours(self, coord: Coord4D, f: Callable[[int], int]):
        cx, cy, cz, cw = coord
        for x in range(-1, 2):
            for y in range(-1, 2):
                for z in range(-1, 2):
                    for w in range(-1, 2):
                        if x == y == z == w == 0:
                            continue
                        c = (cx + x, cy + y, cz + z, cw + w)
                        self.update_neighbour(c, f)


if __name__ == "__main__":
    data = load('day17-test.txt')
    gol = GameOfLife3D(data)
    gol.evolve(6)
    assert gol.active() == 112

    gol = GameOfLife4D(data)
    gol.evolve(6)
    assert gol.active() == 848

    data = load('day17.txt')
    gol = GameOfLife3D(data)
    gol.evolve(6)
    total = gol.active()
    assert total == 322
    print('Active cubes: %d' % total)

    gol = GameOfLife4D(data)
    gol.evolve(6)
    total = gol.active()
    assert total == 2000
    print('Active cubes: %d' % total)
