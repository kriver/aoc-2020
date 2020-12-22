#!/usr/bin/env python3
import re
from typing import List, Dict, Tuple, Set

from util import load

Hand = List[int]


def parse(lines: List[str]) -> Tuple[Hand, Hand]:
    p: List[Hand] = [[], []]
    player = 0
    for line in lines:
        if line.startswith('Player'):
            if line == 'Player 2:':
                player = 1
        elif not line:
            continue
        else:
            p[player].append(int(line))
    return p[0], p[1]


def calc_score(h: Hand) -> int:
    return sum(t[0] * t[1] for t in zip(h, list(range(len(h), 0, -1))))


def combat(h1: Hand, h2: Hand) -> int:
    while h1 and h2:
        p1 = h1.pop(0)
        p2 = h2.pop(0)
        if p1 > p2:
            h1.extend([p1, p2])
        else:
            h2.extend([p2, p1])
    return calc_score(h1 if h1 else h2)


def recursive_combat(h1: Hand, h2: Hand) -> Tuple[Hand, Hand]:
    hashes1 = set()
    hashes2 = set()
    while h1 and h2:
        hash1 = hash(tuple(h1))
        hash2 = hash(tuple(h2))
        if hash1 in hashes1 or hash2 in hashes2:
            return h1, []  # player one wins
        hashes1.add(hash1)
        hashes2.add(hash2)

        p1 = h1.pop(0)
        p2 = h2.pop(0)
        if p1 <= len(h1) and p2 <= len(h2):
            h1b, h2b = recursive_combat(h1[:p1], h2[:p2])
            if h1b:
                h1.extend([p1, p2])
            else:
                h2.extend([p2, p1])
        elif p1 > p2:
            h1.extend([p1, p2])
        else:
            h2.extend([p2, p1])
    return h1, h2


if __name__ == "__main__":
    hand1, hand2 = parse(load('day22-test.txt'))
    assert combat(hand1, hand2) == 306

    hand1, hand2 = parse(load('day22-test.txt'))
    hand1, hand2 = recursive_combat(hand1, hand2)
    assert calc_score(hand1 if hand1 else hand2) == 291

    hand1, hand2 = parse(load('day22.txt'))
    score = combat(hand1, hand2)
    print('Score is %d' % score)

    hand1, hand2 = parse(load('day22.txt'))
    hand1, hand2 = recursive_combat(hand1, hand2)
    score = calc_score(hand1 if hand1 else hand2)
    print('Score is %d' % score)
