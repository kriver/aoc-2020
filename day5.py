#!/usr/bin/env python3

from util import load

ROW_TR = str.maketrans("FB", "01")
COL_TR = str.maketrans("LR", "01")


def code_to_pos(code: str) -> (int, int, int):
    row = int(code[:7].translate(ROW_TR), 2)
    column = int(code[7:].translate(COL_TR), 2)
    return row, column, row * 8 + column


if __name__ == "__main__":
    assert code_to_pos('FBFBBFFRLR') == (44, 5, 357)
    assert code_to_pos('BFFFBBFRRR') == (70, 7, 567)
    assert code_to_pos('FFFBBBFRRR') == (14, 7, 119)
    assert code_to_pos('BBFFBBFRLL') == (102, 4, 820)

    lines = load('day5.txt')
    positions = list(map(code_to_pos, lines))

    min_id = min(positions, key=lambda p: p[2])
    max_id = max(positions, key=lambda p: p[2])
    assert max_id[2] == 980
    print("Lowest/highest seat ID : %d/%d" % (min_id[2], max_id[2]))

    seat_ids = set(map(lambda p: p[2], positions))
    seat_id = -1
    for seat_id in range(min_id[2], max_id[2]):
        if seat_id not in seat_ids:
            break
    assert seat_id == 607
    print("Your seat ID: %d" % seat_id)
