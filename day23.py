#!/usr/bin/env python3
from typing import List, Dict, Tuple


def play(cups: List[int], rounds: int) -> List[int]:
    num_cups = len(cups)
    current = 0
    for i in range(rounds):
        current_label = cups[current]
        label = current_label - 1
        the_three = (cups + cups)[current + 1:current + 4]
        if current + 4 <= num_cups:
            the_other = cups[:current + 1] + cups[current + 4:]
        else:
            the_other = cups[(current + 4) % num_cups:current + 1]
        while True:
            try:
                idx = the_other.index(label)
                break
            except ValueError:
                label = label - 1 if label > 1 else num_cups
        cups = the_other[:idx + 1] + the_three + the_other[idx + 1:]
        # print('%2d - Pick %d=%d : %s -> %s' %
        #       (i + 1, current, current_label, the_three, cups))
        current = (cups.index(current_label) + 1) % num_cups
        assert len(cups) == num_cups
    return cups


def parse(data: str) -> List[int]:
    return [int(c) for c in data]


class Node:
    def __init__(self, num: int, prev_node: int, next_node: int):
        self.num = num
        self.prev = prev_node
        self.next = next_node

    def __repr__(self):
        return '%d <- %d -> %d' % (self.prev, self.num, self.next)


LinkedList = Dict[int, Node]


def to_linked_list(data: str, max_num: int) -> LinkedList:
    llist = {i: Node(i, (i - 2) % max_num + 1, i % max_num + 1)
             for i in range(1, max_num + 1)}
    cups = [int(c) for c in data]
    num_cups = len(cups)
    for i in range(num_cups):
        cup = cups[i]
        llist[cup].prev = cups[(i - 1) % num_cups]
        llist[cup].next = cups[(i + 1) % num_cups]
    llist[cups[0]].prev = max_num
    llist[max_num].next = cups[0]
    llist[num_cups + 1].prev = cups[num_cups - 1]
    llist[cups[num_cups - 1]].next = num_cups + 1
    return llist


def to_str(cups: LinkedList) -> str:
    s = ''
    idx = 1
    while True:
        s += str(cups[idx].num)
        idx = cups[idx].next
        if idx == 1:
            break
    return s


def play2(cups: LinkedList, current_label: int, max_num: int, rounds: int) \
        -> Tuple[int, int]:
    for i in range(rounds):
        picked: List[int] = [0, 0, 0]
        picked[0] = cups[current_label].next
        picked[1] = cups[picked[0]].next
        picked[2] = cups[picked[1]].next
        label = current_label
        while True:
            label = label - 1 if label > 1 else max_num
            if label not in picked:
                break
        # remove three cups
        after_three = cups[picked[2]].next
        cups[current_label].next = after_three
        cups[after_three].prev = current_label
        # insert three cups
        old_next = cups[label].next
        cups[label].next = cups[picked[0]].num
        cups[picked[0]].prev = label
        cups[picked[2]].next = old_next
        cups[old_next].prev = cups[picked[2]].num
        if i % 100_000 == 0:
            print('%2d - Pick %d : %s' % (i + 1, current_label, picked))
        current_label = cups[current_label].next
    result1 = cups[1].next
    result2 = cups[result1].next
    return result1, result2


def to_result(cups: List[int]) -> str:
    idx = cups.index(1)
    return ''.join(str(i) for i in cups[idx + 1:] + cups[:idx])


if __name__ == "__main__":
    # part 1
    assert to_result(play(parse('389125467'), 10)) == '92658374'
    assert to_result(play(parse('389125467'), 100)) == '67384529'

    result = to_result(play(parse('253149867'), 100))
    assert result == '34952786'
    print('Arrangement is %s' % result)

    # part 2
    MAX = 1_000_000
    assert play2(to_linked_list('389125467', MAX), 3, MAX, 10_000_000) == (934001, 159792)
    result = play2(to_linked_list('253149867', MAX), 2, MAX, 10_000_000)
    assert result == (595814, 848141)
    print('Cups after 1 are %d and %d -> %d'
          % (result[0], result[1], result[0] * result[1]))
