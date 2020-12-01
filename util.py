def load(filename):
    with open('data/' + filename, 'r') as f:
        lines = f.read().splitlines()
    return lines


def as_int(l):
    return list(map(lambda x: int(x), l))
