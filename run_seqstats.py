#!/usr/bin/env python3

from seqstats import main
import sys
from multiprocessing import Pool
import pandas as pd
import os
import time
from myio import get_path

if __name__ == '__main__':
    t1 = time.time()
    ch = sys.argv[1]

    n_core = 3
    pool = Pool(n_core)

    args = [{'ch': ch, 'chunk': i, 'n_chunk': n_core} for i in range(n_core)]
    results = pool.map(main, args)

    out = {k: [] for k in results[0].keys()}

    for r in results:
        for k, v in out.items():
            out[k].append(r[k])

    path = get_path()
    for k, v in out.items():
        fpath = os.path.join(
            path['out'], 'chr_{ch}_{k}.csv'.format(ch=ch, k=k))
        pd.concat(v).to_csv(fpath)

    t2 = time.time()
    fpath = os.path.join(
        path['out'], 'chr_{ch}_runtime_seqstats.csv'.format(ch=ch))
    with open(fpath, 'w') as f:
        f.write('{:0.1f}\n'.format(t2-t1))
