import numpy as np


def partition(n):
    """
Integer partitions of a number.

Parameters:
    n (int)

Returns:
        (list of tuples)

Example:
    partition(3) -> [(3,), (2, 1), (1, 1, 1)]
"""
    answer = set()
    answer.add((n, ))
    for x in range(1, n):
        for y in partition(n - x):
            answer.add(tuple(sorted((x, ) + y, reverse=True)))
    return sorted(list(answer), key=lambda x: (-x[0], len(x)))


def partition_repr(x):
    if isinstance(x, tuple):
        return '{' + ','.join([str(i) for i in x]) + '}'
    if isinstance(x, int):
        return [partition_repr(p) for p in partition(x)]


def partition_map(x):
    return {p: partition_repr(p) for p in partition(x)}


class Parititon:
    def __init__(self, n):
        self.n = n
        self.part = partition(self.n)
        self.repr = partition_repr(self.n)
        self.map = partition_map(self.n)


if __name__ == '__main__':
    for z in range(2, 6+1):
        print("number of int partitions of %d is %d" % (z, len(partition(z))))
    for i, p in enumerate(partition_repr(6)):
        print(i+1, p)
