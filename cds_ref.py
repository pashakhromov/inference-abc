#!/usr/bin/env python3

import pandas as pd
import numpy as np
import seqtools
import os
import sys
import socket
from Bio import SeqIO

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

ch = '2L'
path = get_path()

def load_data(name):
    df = pd.read_csv(os.path.join(path['in'], '{}.csv'.format(name)), index_col=0)
    df['len'] = df.end - df.start + 1
    return df

cds = load_data('cds')
cds = cds[cds.ch == ch]

seq = {}
seq_ref = ''
with open(os.path.join(path['in'], 'chr_{}.fasta'.format(ch)), 'r') as f:
    for record in SeqIO.parse(f, 'fasta'):
        des = record.description
        if 'ref' in des.lower():
            seq_ref = record.seq
        else:
            seq[des] = record.seq


stat = {
    'n_mut'   : {},
    'n_non_na': {},
}

t1 = time.time()
c = 0
for K, V in cds[cds.ch == ch].iterrows():
    bp = slice(V.start, V.end+1)
    lst_ = {}
    str_ = {}
    for k, v in seq.items():
        s = v[bp]
        lst_[k] = list(s)
        str_[k] = str(s)
    lst_ = pd.DataFrame(lst_).T
    lst_ = seqtools.drop_na_seq(lst_)
    str_ = pd.Series(str_).loc[lst_.index]

    lst_ref = pd.DataFrame(
        {'ref': list(seq_ref[bp])}).T
    lst_ref[lst_ref == 'N'] = np.nan

    if 'n_mut' in stat.keys():
        stat['n_mut'][K] = seqtools.n_mutations(lst_, lst_ref)
    if 'n_non_na' in stat.keys():
        stat['n_non_na'][K] = lst_.shape[0]
    
    # if c > 100:
    #     break
    # c += 1

for k, v in stat.items():
    if k in ['sample']:
        pd.DataFrame(v).T.to_csv('chr_{ch}_{k}.csv'.format(ch=ch, k=k))
    else:
        pd.Series(v).to_csv(os.path.join(path['out'], 'cds_ref_{}.csv'.format(k)))

t2 = time.time()

with open(os.path.join(path['out'], 'runtime_cds_ref.csv'), 'w') as f:
    f.write('runtime={dt:0.1f}\nn_seq={n_seq}\n'.format(dt=t2-t1, n_seq=len(seq)))