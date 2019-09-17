from seqstats import main
import sys
from multiprocessing import Pool

if __name__ == '__main__':
    ch = sys.argv[1]

    n_core = 3
    pool = Pool(n_core)

    args = [{'ch': ch, 'chunk': i, 'n_chunk': n_core} for i in range(n_core)]

    # print(args)
    # results = pool.map(main, zip(a, b))
    results = pool.map(main, args)
