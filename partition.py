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
    answer.add((n,))
    for x in range(1, n):
        for y in partition(n - x):
            answer.add(tuple(sorted((x,) + y, reverse=True)))
    return sorted(list(answer), key=lambda x: (-x[0], len(x)))


def partition_repr(x):
    """
    Pretty print for integer partition.
    If int tuple is passed, it formats it (2, 1) -> '{2,1}'.
    If int is passed, calculates its partition and formats all tuples in the partition:
    3 -> [(3,), (2, 1), (1, 1, 1)] -> ['{3}', '{2,1}', '{1,1,1}']

    Parameters:
        x (tuple of ints / int) 

    Returns:
        (str / list of str)

    Example:
        partition_repr((2, 1)) -> '{2,1}'
        partition_repr(3) -> ['{3}', '{2,1}', '{1,1,1}']
    """
    if isinstance(x, tuple):
        return '{' + ','.join([str(i) for i in x]) + '}'
    if isinstance(x, int):
        return [partition_repr(p) for p in partition(x)]


def partition_map(n):
    """
    Provides mapping between partition and its pretty print.

    Parameters:
        n (int) 

    Returns:
        (dict)

    Example:
        partition_map(3) -> {(3,): '{3}', (2, 1): '{2,1}', (1, 1, 1): '{1,1,1}'}
    """
    return {p: partition_repr(p) for p in partition(n)}


class Partition:
    def __init__(self, n):
        self.n = n
        self.part = partition(self.n)
        self.repr = partition_repr(self.n)
        self.map = partition_map(self.n)

    def __repr__(self):
        return 'Partition({})'.format(self.n)


if __name__ == '__main__':
    for n in range(2, 6 + 1):
        print("number of integer partitions of {n} is {n_par}".format(n=n, n_par=len(partition(n))))
    for i, p in enumerate(partition_repr(6)):
        print(i + 1, p)
