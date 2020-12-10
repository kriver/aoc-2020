#!/usr/bin/env python3
from itertools import groupby
from typing import List, Dict, Set

from util import load, as_int


def rating_for(data: List[int]) -> List[int]:
    inputs = [0] + data
    outputs = data + [data[-1] + 3]
    in_outs = zip(inputs, outputs)
    deltas = map(lambda io: io[1] - io[0], in_outs)
    sorted_deltas = sorted(deltas)
    counts = [-1] * 4
    for k, v in groupby(sorted_deltas):
        counts[k] = len(list(v))
    return counts


def count_paths(data: Dict[int, List[int]], node: int, dst: int) -> int:
    if node == dst:
        return 1
    # all possible sources to reach this node
    srcs = data[node]
    lengths = map(lambda n: count_paths(data, n, dst), srcs)
    # l = list(lengths)
    return sum(lengths)


def partition_by_src(src: int, data: Dict[int, List[int]], processed: Set[int]):
    if src not in processed:
        processed.add(src)
        if len(data[src]) > 1:
            for i in data[src]:
                partition_by_src(i, data, processed)


def paths_for(data: List[int]) -> int:
    ext_data = [0] + data + [data[-1] + 3]
    # build map of reachable nodes (reversed)
    reverse_paths = {k: [] for k in ext_data}
    for n in ext_data:
        for offset in range(1, 4):
            if n + offset in reverse_paths:
                reverse_paths[n + offset].append(n)
    # partition this into sub-graphs
    # for each sub-graph, count the paths and multiply
    total = 1
    processed = set()
    for k in reversed(sorted(reverse_paths.keys())):
        if k in processed:
            continue
        v = reverse_paths[k]
        if len(v) > 1:
            newly_processed = set()
            partition_by_src(k, reverse_paths, newly_processed)
            processed |= newly_processed
            cnt = count_paths(reverse_paths, max(newly_processed), min(newly_processed))
            total *= cnt
        else:
            processed.add(k)
    return total


if __name__ == "__main__":
    joltages = sorted(as_int(load('day10-test.txt')))
    ratings = rating_for(joltages)
    assert 1 * ratings[1] + 3 * ratings[3] == 22
    paths = paths_for(joltages)
    assert paths == 8

    joltages = sorted(as_int(load('day10-test2.txt')))
    ratings = rating_for(joltages)
    assert ratings[1] * ratings[3] == 220
    paths = paths_for(joltages)
    assert paths == 19208

    joltages = sorted(as_int(load('day10.txt')))
    ratings = rating_for(joltages)
    assert ratings[1] * ratings[3] == 2244
    print("Rating: %d" % (ratings[1] * ratings[3]))
    paths = paths_for(joltages)
    assert paths == 3_947_645_370_368
    print("Paths: %d" % paths)
