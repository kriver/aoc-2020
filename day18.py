#!/usr/bin/env python3
import re
from typing import Callable, List, Tuple

from util import load

NUMBER = r'^\d+$'


def add(a: int, b: int) -> int:
    return a + b


def multiple(a: int, b: int) -> int:
    return a * b


def tokenize(line: str) -> List[str]:
    tokens = []
    prev = None
    for c in line:
        if c == ' ':
            continue
        if '0' <= c <= '9':
            prev = prev * 10 + int(c) if prev else int(c)
        else:
            if prev:
                tokens.append(str(prev))
                prev = None
            tokens.append(c)
    if prev:
        tokens.append(str(prev))
    return tokens


def eval_tokens_part1(tokens: List[str], i=0, nesting=0) -> Tuple[int, int]:
    result = None
    operator: Callable[[int, int], int] = None
    while True:
        token = tokens[i]
        if re.match(NUMBER, token):
            if not result:
                result = int(token)
            else:
                result = operator(result, int(token))
        elif '+' == token:
            operator = add
        elif '*' == token:
            operator = multiple
        elif '(' == token:
            nested, i = eval_tokens_part1(tokens, i + 1, nesting + 1)
            if not result:
                result = nested
            else:
                result = operator(result, nested)
        elif ')' == token:
            return result, i
        else:
            raise RuntimeError(token)
        i += 1
        if i >= len(tokens):
            break
    return result, i


def eval_part1(line: str) -> int:
    return eval_tokens_part1(tokenize(line))[0]


def eval_tokens_part2(tokens: List[str], i=0, nesting=0) -> Tuple[int, int]:
    result = None
    operator: Callable[[int, int], int] = None
    while True:
        token = tokens[i]
        if re.match(NUMBER, token):
            if not result:
                result = int(token)
            else:
                result = operator(result, int(token))
        elif '+' == token:
            operator = add
        elif '*' == token:
            nested, i = eval_tokens_part2(tokens, i + 1, nesting + 1)
            result = multiple(result, nested)
            return result, i
        elif '(' == token:
            nested, i = eval_tokens_part2(tokens, i + 1, nesting + 1)
            if not result:
                result = nested
            else:
                result = operator(result, nested)
        elif ')' == token:
            return result, i
        else:
            raise RuntimeError(token)
        i += 1
        if i >= len(tokens):
            break
    return result, i


def eval_part2(line: str) -> int:
    return eval_tokens_part2(tokenize(line))[0]


if __name__ == "__main__":
    assert eval_part1('2 * 3 + (4 * 5)') == 26
    assert eval_part1('5 + (8 * 3 + 9 + 3 * 4 * 3)') == 437
    assert eval_part1('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))') == 12240
    assert eval_part1(
        '((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2') == 13632

    data = load('day18.txt')
    total = sum(map(eval_part1, data))
    assert total == 12956356593940
    print('Total is %d' % total)

    assert eval_part2('1 + (2 * 3) + (4 * (5 + 6))') == 51
    assert eval_part2('2 * 3 + (4 * 5)') == 46
    assert eval_part2('5 + (8 * 3 + 9 + 3 * 4 * 3)') == 1445
    assert eval_part2('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))') == 669060
    assert eval_part2('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2') == 23340

    total = sum(map(eval_part2, data))
    assert total == 94240043727614
    print('Total is %d' % total)
