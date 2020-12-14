#!/usr/bin/env python3
import re
from typing import Dict, List, Tuple

from util import load

MASK_RE = re.compile(r'^mask = ([01X]+)$')
MEM_RE = re.compile(r'^mem\[(\d+)\] = (\d+)$')

X_TO_0 = str.maketrans('X', '0')
X_TO_1 = str.maketrans('X', '1')


def run_1(lines: List[str]) -> Dict[int, int]:
    def parse_mask(s: str) -> Tuple[int, int]:
        or_mask = int(s.translate(X_TO_0), 2)
        and_mask = int(s.translate(X_TO_1), 2)
        return or_mask, and_mask

    mem = {}
    mask = (0, 2 << 36 - 1)
    for line in lines:
        m = re.match(MASK_RE, line)
        if m:
            mask = parse_mask(m.group(1))
        else:
            m = re.match(MEM_RE, line)
            if m:
                address = int(m.group(1))
                value = int(m.group(2))
                value = (value | mask[0]) & mask[1]
                mem[address] = value
            else:
                print("ERR - %s" % line)
                raise RuntimeError
    return mem


def run_2(lines: List[str]) -> Dict[int, int]:
    def parse_mask(s: str) -> Tuple[int, List[int]]:
        or_mask = int(s.translate(X_TO_0), 2)
        noise_mask = [35 - i for i, c in enumerate(s) if c == 'X']
        return or_mask, noise_mask

    def all_addresses(addr: List[int], noises: List[int]) -> List[int]:
        if not noises:
            return addr
        bit = noises[0]
        or_mask = 1 << bit
        and_mask = (2 ** 36 - 1) ^ or_mask
        new_addr = [a | or_mask for a in addr] + [a & and_mask for a in addr]
        return all_addresses(new_addr, noises[1:])

    def set_mem(addr: int, val: int):
        for a in all_addresses([addr], mask[1]):
            mem[a] = val

    mem = {}
    mask = (0, [])
    for line in lines:
        m = re.match(MASK_RE, line)
        if m:
            mask = parse_mask(m.group(1))
        else:
            m = re.match(MEM_RE, line)
            if m:
                address = int(m.group(1))
                value = int(m.group(2))
                address = address | mask[0]
                set_mem(address, value)
            else:
                print("ERR - %s" % line)
                raise RuntimeError
    return mem


def mem_sum(mem: Dict[int, int]) -> int:
    return sum(mem.values())


if __name__ == "__main__":
    data = load('day14-test.txt')
    memory = run_1(data)
    total = mem_sum(memory)
    assert total == 165

    data = load('day14-test2.txt')
    memory = run_2(data)
    total = mem_sum(memory)
    assert total == 208

    data = load('day14.txt')
    memory = run_1(data)
    total = sum(memory.values())
    assert total == 7611244640053
    print('Total is %d' % total)

    memory = run_2(data)
    total = sum(memory.values())
    assert total == 3705162613854
    print('Total is %d' % total)
