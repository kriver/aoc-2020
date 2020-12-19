#!/usr/bin/env python3
import itertools
from typing import List, Tuple, Dict

from util import as_int, load

Rule = Tuple[List[List[int]], str]

AB_BITS = str.maketrans('ab', '01')


def parse_rule(s: str) -> Tuple[int, Rule]:
    l = s.split(':')
    final = None
    rule_id = int(l[0])
    ored = [s.strip() for s in l[1].split('|')]
    if len(ored) == 1 and ored[0][0] == '"':
        final = ored[0][1]
        anded = []
    else:
        anded = [as_int(o.split(' ')) for o in ored]
    return rule_id, (anded, final)


def parse(lines: List[str]) -> Tuple[Dict[int, Rule], List[str]]:
    r = {}
    m = []
    parsing_rules = True
    for line in lines:
        if line == '':
            parsing_rules = False
            continue
        if parsing_rules:
            rule_id, rule = parse_rule(line)
            r[rule_id] = rule
        else:
            m.append(line)
    return r, m


def expand_rule(rules: Dict[int, Rule], num: int) -> List[str]:
    def final(rule: Rule) -> bool:
        return rule[1] is not None

    def ored(l: List[List[int]]) -> List[str]:
        x = [anded(o) for o in l]
        y = [item for sublist in x for item in sublist]
        return y

    def anded(l: List[int]) -> List[str]:
        x = [recurse(i) for i in l]
        y = itertools.product(*x)
        z = [''.join(s) for s in y]
        return z

    def recurse(n: int) -> List[str]:
        r = rules[n]
        if final(r):
            return [r[1]]
        return ored(r[0])

    return recurse(num)


def to_nums(s: str) -> List[int]:
    assert len(s) % 8 == 0
    bits = s.translate(AB_BITS)
    return [int(bits[i:i + 8], 2) for i in range(0, len(bits), 8)]


if __name__ == "__main__":
    the_rules, msgs = parse(load('day19-test.txt'))

    assert expand_rule(the_rules, 4) == ['a']
    assert expand_rule(the_rules, 5) == ['b']
    assert expand_rule(the_rules, 1) == ['aaab', 'aaba', 'bbab', 'bbba',
                                         'abaa', 'abbb', 'baaa', 'babb']
    assert expand_rule(the_rules, 0) == ['aaaabb', 'aaabab', 'abbabb', 'abbbab',
                                         'aabaab', 'aabbbb', 'abaaab', 'ababbb']
    rule0 = set(expand_rule(the_rules, 0))
    matches0 = len(list(filter(lambda m: m in rule0, msgs)))
    assert matches0 == 2

    the_rules, msgs = parse(load('day19.txt'))
    rule0 = set(expand_rule(the_rules, 0))
    matches0 = len(list(filter(lambda m: m in rule0, msgs)))
    assert matches0 == 224
    print('Matching rule 0 : %d/%d' % (matches0, len(msgs)))

    # -- Part 2 --

    # 8: 42 | 42 8
    # 8: 42{1,n}
    the_rules[8] = [[42], [42, 8]], None
    # 11: 42 31 | 42 11 31
    # 11: 42{1,n} 31{1,n}
    the_rules[11] = [[42, 31], [42, 11, 31]], None

    matches42 = set(expand_rule(the_rules, 42))
    len42 = {len(s) for s in matches42}
    assert len(len42) == 1
    len42 = len42.pop()
    assert len42 == 8
    # nums42 = list(sorted([to_nums(m)[0] for m in matches42]))

    matches31 = set(expand_rule(the_rules, 31))
    len31 = {len(s) for s in matches31}
    assert len(len31) == 1
    len31 = len31.pop()
    assert len31 == 8
    # nums31 = list(sorted([to_nums(m)[0] for m in matches31]))

    # 0: 8 11
    # 0: 42{2,n} 31{1,n}
    # -> also number of 42 at least one more than number of 31
    matches0 = 0
    for msg in msgs:
        assert len(msg) % 8 == 0
        count42 = 0
        while msg[:len42] in matches42:
            msg = msg[len42:]
            count42 += 1
        if count42 < 2:
            continue
        count31 = 0
        while msg[:len31] in matches31:
            msg = msg[len31:]
            count31 += 1
        if count31 < 1:
            continue
        if count42 <= count31:
            continue
        if not msg:
            matches0 += 1

    assert matches0 == 436
    print('Matching rule 0 : %d/%d' % (matches0, len(msgs)))
