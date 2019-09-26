#!/usr/bin/env python3

import pandas as pd
import numpy as np
import seqtools
import os
import sys
from Bio import SeqIO
import time
from myio import get_path, read_series, read_df


def main(args):
    ch = args['ch']
    chunk = int(args['chunk'])
    n_chunk = int(args['n_chunk'])

    path = get_path()
    data = pd.read_csv(os.path.join(
        path['in'], 'chr_{}_data.csv'.format(ch)), **read_series)

    w_size = 100
    n_win = data.l_chr // w_size
    n_seq = data.n_seq

    d = {
        'ch': ch,
        'w_size': w_size,
        'n': n_win,
        'chunk': chunk,
        'w1': chunk * n_win // n_chunk,
        'w2': (chunk+1) * n_win // n_chunk,
        'l': data.l_chr,
    }
    d['x1'] = d['w1'] * w_size
    d['x2'] = d['w2'] * w_size
    d['x2'] = min(d['x2'], data.l_chr)
    wins = range(d['w1'], d['w2'])
    bps = slice(d['x1'], d['x2'])
    # msg = (
    #     'Chromosome {ch}: '
    #     'Number of bp {l:,} or '
    #     '{n:,} windows of size {w_size}\n'
    #     'Processing chunk {chunk}: '
    #     '{x1:,} <= bp < {x2:,} or {w1:,} <= w < {w2:,}'.format(**d)
    # )

    seq = {}
    seq_ref = ''
    with open(os.path.join(path['in'], 'chr_{}.fasta'.format(ch)), 'r') as f:
        for record in SeqIO.parse(f, 'fasta'):
            des = record.description
            if 'ref' in des.lower():
                seq_ref = record.seq[bps]
            else:
                seq[des] = record.seq[bps]

    # return msg, len(seq), len(seq_ref), seq_ref[:3]
    stat = {
        'watterson': {},
        'tajima': {},
        'n_mut': {},
        'n_non_na': {},
        'sample': {},
    }

    # c, c_max = 0, 50
    for w in wins:
        bp = slice(w*w_size, (w+1)*w_size)
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

        if 'watterson' in stat.keys():
            stat['watterson'][w] = seqtools.watterson(lst_)
        if 'tajima' in stat.keys():
            stat['tajima'][w] = seqtools.tajima(lst_)
        if 'n_mut' in stat.keys():
            stat['n_mut'][w] = seqtools.n_mutations(lst_, lst_ref)
        if 'n_non_na' in stat.keys():
            stat['n_non_na'][w] = lst_.shape[0]
        if 'sample' in stat.keys():
            stat['sample'][w] = seqtools.encode_sample(
                str_, pad_with_nan=True, sample_size=n_seq)

        # if c > c_max:
        #     break
        # c += 1

    stat = {k: pd.DataFrame({k: v}) for k, v in stat.items()}
    return stat


if __name__ == '__main__':
    pass
