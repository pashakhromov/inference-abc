#!/usr/bin/env python3
import socket
from multiprocessing import Pool
import pandas as pd
import os
import time


def get_path():
    if socket.gethostname() == 'laptopus':
        return {
            'sim': '/home/pasha/Desktop/phd/sim_data',
            'in': '/home/pasha/Desktop/phd/chr_data',
            'out': '/home/pasha/Desktop/phd/chr_data/test',
        }
    if socket.gethostname() == 'Ulysses':
        return {
            'sim': '/Users/pasha/Desktop/phd/sim_data',
            'in': '/Users/pasha/Desktop/phd/chr_data',
            'out': '/Users/pasha/Desktop/phd/chr_data/test',
        }
    else:
        return {
            'sim': '/home/pasha/sim_data',
            'in': '/home/pasha/chr_data',
            'out': '/home/pasha/chr_data',
        }


read_series = {
    'index_col': 0,
    'header': None,
    'squeeze': True,
}

read_df = {
    'index_col': 0,
}


def run(var):
    ch = var['ch']
    block = var['block']
    n_core = var['n_core']
    fun = var['fun']

    t1 = time.time()

    pool = Pool(n_core)

    args = [{**var, **{'chunk': i, 'n_chunk': n_core}} for i in range(n_core)]
    results = pool.map(fun, args)

    out = {k: [] for k in results[0].keys()}

    for r in results:
        for k, v in out.items():
            out[k].append(r[k])

    path = get_path()
    for k, v in out.items():
        fpath = os.path.join(path['out'], 'chr_{ch}_{k}.csv'.format(ch=ch, k=k))
        pd.concat(v).to_csv(fpath)

    t2 = time.time()
    fpath = os.path.join(path['out'], 'chr_{ch}_runtime_{block}.csv'.format(ch=ch, block=block))
    with open(fpath, 'w') as f:
        f.write('{:0.1f}\n'.format(t2-t1))


if __name__ == '__main__':
    pass
