#!/usr/bin/env python3
import re
from typing import List, Dict, Tuple

from util import load

Grid = List[str]

TO_BITS = str.maketrans('.#', '01')
DIMENSION = 10

NESSIE = [
    re.compile(r'..................#.'),
    re.compile(r'#....##....##....###'),
    re.compile(r'.#..#..#..#..#..#...')
]


# Orientations
#
#          N E S W
#          0 1 2 3
# opposite          +2 %4
#          2 3 0 1
#          S W N E

def rotate_cw(grid: Grid) -> Grid:
    zipped = zip(*reversed(grid))
    return [''.join(z) for z in zipped]


def flip(grid: Grid, east_west: bool):
    if east_west:
        return [row[::-1] for row in grid]
    else:
        return list(reversed(grid))


class Tile:
    def __init__(self, num: int, grid: Grid):
        self._id: int = num
        self._grid: Grid = grid
        self._calc_borders()
        self._rotation = 0
        self._flipped = False

    @staticmethod
    def _to_num(s: str) -> int:
        return int(s.translate(TO_BITS), 2)

    def id(self):
        return self._id

    def border(self, b: int):
        return self._border[b]

    def has_border(self, b: int) -> Tuple[bool, bool]:
        if b in self._border:
            return True, False
        if b in self._flip_border:
            return True, True
        return False, False

    def _calc_borders(self):
        rotated = rotate_cw(self._grid)
        self._border: List[int] = [self._to_num(self._grid[0]),
                                   self._to_num(rotated[DIMENSION - 1]),
                                   self._to_num(self._grid[DIMENSION - 1]),
                                   self._to_num(rotated[0])]
        self._flip_border: List[int] = [self._to_num(self._grid[0][::-1]),
                                        self._to_num(rotated[DIMENSION - 1][::-1]),
                                        self._to_num(self._grid[DIMENSION - 1][::-1]),
                                        self._to_num(rotated[0][::-1])]

    # rotate self so border is at new_location
    def rotate(self, other_border: int, new_location: int):
        try:
            current_location = self._border.index(other_border)
        except ValueError:
            current_location = self._flip_border.index(other_border)
        rotations = (new_location - current_location) % 4
        g = self._grid
        for i in range(rotations):
            g = rotate_cw(g)
        self._grid = g
        self._calc_borders()
        self._rotation = rotations

    def flip(self, east_west: bool):
        self._grid = flip(self._grid, east_west)
        self._flipped = True
        self._calc_borders()


Tiles = Dict[int, Tile]
Coord = Tuple[int, int]


class Photo:
    def __init__(self, tiles: Tiles):
        self._tiles: Tiles = tiles
        self._grid: Dict[Coord, int] = {}
        self._min = (0, 0)
        self._max = (0, 0)
        self._image: Grid = []

    # For a newly placed tile, find its neighbours (recursively)
    def _arrange_r(self, coord: Coord, tiles: List[Tile]) -> List[Tile]:
        if not tiles:
            return []
        current_tile = self._tiles[self._grid[coord]]
        for i, delta in enumerate([(0, 1), (1, 0), (0, -1), (-1, 0)]):
            neighbour = coord[0] + delta[0], coord[1] + delta[1]
            if neighbour in self._grid:
                continue
            b = current_tile.border(i)
            matches = [t for t in tiles if t.has_border(b)[0]]
            if not matches:
                continue
            match = matches[0]
            tiles = [t for t in tiles if t != match]  # remove
            # ensure correct rotation
            opposite = (i + 2) % 4  # N<->S, E<->W
            tile = self._tiles[match.id()]
            tile.rotate(b, opposite)
            # ensure correct flipping
            _, flipped = match.has_border(b)
            if flipped:
                tile.flip(i % 2 == 0)
            # Found one, recurse
            self._min = min(self._min[0], neighbour[0]), \
                        min(self._min[1], neighbour[1])
            self._max = max(self._max[0], neighbour[0]), \
                        max(self._max[1], neighbour[1])
            self._grid[neighbour] = match.id()
            tiles = self._arrange_r(neighbour, tiles)
        return tiles

    def arrange(self):
        tiles = list(self._tiles.values())
        center = (0, 0)
        self._grid[center] = tiles[0].id()
        self._arrange_r(center, tiles[1:])

    def corner_product(self):
        return self._grid[self._min[0], self._min[1]] * \
               self._grid[self._min[0], self._max[1]] * \
               self._grid[self._max[0], self._max[1]] * \
               self._grid[self._max[0], self._min[1]]

    def recompose(self):
        min_x, min_y = self._min
        max_x, max_y = self._max
        self._image = [''] * ((max_y - min_y + 1) * (DIMENSION - 2))
        for y in range(0, max_y - min_y + 1):
            for x in range(0, max_x - min_x + 1):
                tile = self._tiles[self._grid[min_x + x, min_y + y]]
                # Part one is designed with XY-axes pointing (N,E), recomposing
                # the full image needs to flow the Y-axis south.
                for i, row in enumerate(reversed(tile._grid[1:-1])):
                    self._image[y * (DIMENSION - 2) + i] += row[1:-1]
        print('Image size is (%d, %d)' % (len(self._image[0]), len(self._image)))

    @staticmethod
    def _count_monsters(image: Grid) -> int:
        monsters: List[Coord] = []
        for i, line in enumerate(image[2:]):
            offset = 0
            while True:
                m = re.search(NESSIE[2], line[offset:])
                if not m:
                    break
                # print(0, "$$", NESSIE[0], "$$", image[i], "$$", i)
                # print(0, "$$", NESSIE[1], "$$", image[i + 1], "$$", i + 1)
                # print(m.start(), "$$", NESSIE[2], "$$", line, "$$", i + 2)
                if re.match(NESSIE[0], image[i][offset + m.start():]) and \
                        re.match(NESSIE[1], image[i + 1][offset + m.start():]):
                    coord = m.start(), i
                    print('Found monster at (%d, %d)' % coord)
                    monsters.append(coord)
                    offset += m.end()
                else:
                    offset += m.start() + 1
        return len(monsters)

    def find_monsters(self):
        count = 0
        # try 4 orientations, and for each also the flipped version
        image = self._image
        for rotation in range(4):
            count = Photo._count_monsters(image)
            if count > 0:
                print('Found %d monsters (%d)' % (count, rotation))
                break
            flipped = flip(image, False)
            count = Photo._count_monsters(flipped)
            if count > 0:
                print('Found %d monsters (%dF)' % (count, rotation))
                break
            image = rotate_cw(image)
        return count

    def count_waves(self):
        monsters = self.find_monsters()
        total = sum(len(row.replace('.', '')) for row in self._image)
        return total - monsters * 15


def parse_tiles(lines: List[str]) -> Tiles:
    tile_re = re.compile(r'^Tile (\d+):$')
    tiles: Dict[int, Tile] = {}
    rows = []
    num = 0
    for line in lines:
        m = re.match(tile_re, line)
        if m:
            if rows:
                tiles[num] = Tile(num, rows)
                rows = []
            num = int(m.group(1))
        elif line == '':
            continue
        else:
            rows.append(line)
    if rows:
        tiles[num] = Tile(num, rows)
    return tiles


if __name__ == "__main__":
    assert rotate_cw(['12', '34']) == ['31', '42']

    photo = Photo(parse_tiles(load('day20-test.txt')))
    photo.arrange()
    corner_product = photo.corner_product()
    assert corner_product == 20899048083289
    photo.recompose()
    waves = photo.count_waves()
    assert waves == 273

    photo = Photo(parse_tiles(load('day20.txt')))
    photo.arrange()
    corner_product = photo.corner_product()
    assert corner_product == 59187348943703
    print('Corner product is %d' % corner_product)
    photo.recompose()
    waves = photo.count_waves()
    assert waves == 1565
    print('Number of waves is %d' % waves)
