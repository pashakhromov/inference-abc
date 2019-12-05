#!/usr/bin/env python3

import pandas as pd
from seqtools import sample2hist
import os
import socket

import time

ch = '2L'
n_itr = 10000
resample_size = 5
n_subset = 0


def calc_and_write_hist(ch, n_itr=10000, resample_size=5, n_subset=0):
    if socket.gethostname() == 'laptopus':
        path = '/home/pasha/Desktop/phd/chr_data'
    else:
        path = '/home/pasha/chr_data'
    
    t1 = time.time()

    sample = pd.read_csv(os.path.join(path, 'chr_{}_sample.csv'.format(ch)), index_col=0)

    if n_subset:
        sample = sample.iloc[:n_subset, :]

    hist = sample.apply(lambda x: sample2hist(x, resample_size=resample_size, n_itr=n_itr), axis=1)
    hist.fillna(0).to_csv(os.path.join(path, 'chr_{}_hist.csv'.format(ch)))
    
    t2 = time.time()
    with open(os.path.join(path, 'runtime_hist_{}.txt'.format(ch)), 'w') as f:
        f.write('{:0.2f}\n'.format(t2-t1))
