#!/usr/bin/env python3
import re
from typing import List

from util import *

LINE_REGEX = re.compile(r'^(\d+)-(\d+) (.): (.*)$')


class PasswordWithPolicy:
    def __init__(self, line):
        m = re.match(LINE_REGEX, line)
        if not m:
            raise Exception('invalid input: ' + line)
        self._min = int(m.group(1))
        self._max = int(m.group(2))
        self._char = m.group(3)
        self._password = m.group(4)

    def is_valid_1(self) -> bool:
        return self._min <= self._password.count(self._char) <= self._max

    def is_valid_2(self) -> bool:
        # only one should be true, the other false
        return (self._password[self._min - 1] == self._char) != \
               (self._password[self._max - 1] == self._char)


def parse(filename) -> List[PasswordWithPolicy]:
    lines = load(filename)
    data = []
    for line in lines:
        data.append(PasswordWithPolicy(line))
    return data


if __name__ == "__main__":
    p = PasswordWithPolicy('1-3 a: abc')
    # assert p._min == 1
    # assert p._max == 3
    # assert p._char == 'a'
    # assert p._password == 'abc'
    assert p.is_valid_1()
    assert p.is_valid_2()

    passwords = parse('day2.txt')

    valid_passwords_1 = list(filter(lambda pwp: pwp.is_valid_1(), passwords))
    assert len(valid_passwords_1) == 445
    print("Valid passwords : %d" % (len(valid_passwords_1)))

    valid_passwords_2 = list(filter(lambda pwp: pwp.is_valid_2(), passwords))
    assert len(valid_passwords_2) == 491
    print("Valid passwords : %d" % (len(valid_passwords_2)))
