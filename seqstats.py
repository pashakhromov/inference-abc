#!/usr/bin/env python3

import pandas as pd
from seqtools import sample2hist
import os
import sys
import socket

import time


def get_path():
    if socket.gethostname() == 'laptopus':
        return {
            'sim': '/home/pasha/Desktop/phd/sim_data',
            'in': '/home/pasha/Desktop/phd/chr_data',
            'out': '/home/pasha/Desktop/phd/chr_data/test',
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


def main(args):
    ch = args['ch']
    chunk = int(args['chunk'])
    n_chunk = int(args['n_chunk'])
    
    path = os.path.join(get_path()['in'], 'chr_{}_data.csv'.format(ch))
    data = pd.read_csv(path, **read_series)

    w_size = 100
    n_win = data.l_chr // w_size

    d = {
        'ch': ch,
        'n': n_win,
        'chunk': chunk,
        'w1': chunk * n_win // n_chunk,
        'w2': (chunk+1) * n_win // n_chunk,
    }
    print('Chromosome {ch} has {n:,} windows. Processing chunk {chunk}: {w1:,} <= w < {w2:,}'.format(**d))
    # time.sleep(5)


if __name__ == "__main__":
    # args = {
    #     'ch': sys.argv[1],
    # }
    main(sys.argv[1])
