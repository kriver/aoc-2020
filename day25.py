#!/usr/bin/env python3
from typing import Tuple

from util import load, as_int

Rfid = Tuple[int, int]  # public key and loop count


def transform(subject: int, loops: int) -> int:
    val = 1
    for i in range(loops):
        val = (val * subject) % 20201227
    return val


def guess_loops(subject: int, needle: int) -> int:
    val = 1
    loops = 0
    while val != needle:
        val = (val * subject) % 20201227
        loops += 1
    return loops


def encryption_key(card: Rfid, door: Rfid) -> int:
    card_key = transform(door[0], card[1])
    door_key = transform(card[0], door[1])
    assert card_key == door_key
    print(card_key)
    return card_key


if __name__ == "__main__":
    assert guess_loops(7, 5764801) == 8
    assert guess_loops(7, 17807724) == 11
    assert encryption_key((5764801, 8), (17807724, 11)) == 14897079

    pub_keys = as_int(load('day25.txt'))
    card_rfid = pub_keys[0], guess_loops(7, pub_keys[0])
    door_rfid = pub_keys[1], guess_loops(7, pub_keys[1])
    key = encryption_key(card_rfid, door_rfid)
    print('Encryption key is %d' % key)
