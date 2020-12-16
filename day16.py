#!/usr/bin/env python3
import re
from functools import reduce
from itertools import chain
from typing import Dict, List, Set

from util import load, as_int

TruthRow = List[bool]
TruthMatrix = List[TruthRow]


class Ticket:
    def __init__(self, numbers: List[int]):
        self._numbers: List[int] = numbers

    # Returns:
    # - 1 row per ticket number
    # - each row T/F whether it is in a range
    def classify(self, ranges: List[Set[int]]) -> TruthMatrix:
        return [
            list(map(lambda r: n in r, ranges))
            for n in self._numbers]

    def invalid_numbers(self, ranges: Dict[str, Set[int]]) -> List[int]:
        invalids = []
        for n in self._numbers:
            found = set(map(lambda r: n in r, ranges.values()))
            if True not in found:
                invalids.append(n)
        return invalids


class Document:
    FIELD_RE = re.compile(r'^([a-z ]+): (\d+)-(\d+) or (\d+)-(\d+)$')

    def __init__(self, data: List[str]):
        self._fields: Dict[str, Set[int]] = {}
        i = 0
        # fields
        for i in range(len(data)):
            line = data[i]
            if line == '':
                break
            m = re.match(self.FIELD_RE, line)
            if not m:
                raise RuntimeError
            self._fields[m.group(1)] = \
                set(range(int(m.group(2)), int(m.group(3)) + 1)) | \
                set(range(int(m.group(4)), int(m.group(5)) + 1))
        # your ticket
        assert data[i + 1] == 'your ticket:'
        self._your: Ticket = Ticket(as_int(data[i + 2].split(',')))
        # nearby tickets
        assert data[i + 4] == 'nearby tickets:'
        self._nearby: List[Ticket] = []
        for i in range(i + 5, len(data)):
            line = data[i]
            self._nearby.append(Ticket(as_int(line.split(','))))

    def sum_invalids(self) -> int:
        return sum(chain.from_iterable(
            map(lambda n: n.invalid_numbers(self._fields), self._nearby)))

    def remove_invalids(self):
        self._nearby = list(filter(lambda n: not n.invalid_numbers(self._fields),
                                   self._nearby))

    @staticmethod
    def _combine_row(a: TruthRow, b: TruthRow) -> TruthRow:
        return list(map(lambda t: t[0] and t[1], zip(a, b)))

    @staticmethod
    def _combine_matrix(a: TruthMatrix, b: TruthMatrix) -> TruthMatrix:
        return list(map(lambda t: Document._combine_row(*t), zip(a, b)))

    def _map_to_name(self, classification: TruthMatrix) -> Dict[str, int]:
        mapping: Dict[str, int] = {}
        names = list(sorted(self._fields.keys()))
        counts = [(r.count(True), r) for r in classification]
        done: Set[int] = set()
        for c in sorted(enumerate(counts), key=lambda e: e[1][0]):
            number_idx = c[0]
            row = c[1][1]
            # loop True/False list to determine column, i.e. field
            for i in range(len(row)):
                if i in done:
                    continue
                if row[i]:
                    done.add(i)
                    mapping[names[i]] = number_idx
                    break

        return mapping

    def classify(self):
        sorted_ranges = [self._fields[k] for k in sorted(self._fields.keys())]
        classification = reduce(Document._combine_matrix,
                                map(lambda n: n.classify(sorted_ranges),
                                    self._nearby))
        return self._map_to_name(classification)

    def score(self):
        mapping = self.classify()
        filtered = filter(lambda kv: kv[0].startswith('departure'), mapping.items())
        my_numbers = map(lambda kv: self._your._numbers[kv[1]], filtered)
        return reduce(lambda a, b: a * b, my_numbers)


if __name__ == "__main__":
    data = load('day16-test.txt')
    doc = Document(data)
    result = doc.sum_invalids()
    assert result == 71

    data = load('day16-test2.txt')
    doc = Document(data)
    doc.remove_invalids()
    assert doc.classify() == {'row': 0, 'class': 1, 'seat': 2}

    data = load('day16.txt')
    doc = Document(data)
    result = doc.sum_invalids()
    assert result == 21980
    print('Sum of invalid numbers is %d' % result)

    doc.remove_invalids()
    score = doc.score()
    assert score == 1439429522627
    print('Score is %d' % score)
