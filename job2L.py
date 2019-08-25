import pandas as pd
import numpy as np
from Bio import SeqIO
import seqtools
import os
import time

ch = '2L'
w_size = 100
path = '/home/pasha/chr_data'

seq = {}
seq_ref = ''

with open(os.path.join(path, 'chr_{}.fasta'.format(ch)), 'r') as f:
    for record in SeqIO.parse(f, 'fasta'):
        des = record.description
        if 'ref' in des.lower():
            seq_ref = record.seq
        else:
            seq[des] = record.seq

l_chr = np.unique([len(v) for v in seq.values()])[0]
n_seq = len(seq)
n_win = l_chr // w_size
pd.Series({
    'l_chr': l_chr,
    'n_seq': n_seq,
}).to_csv('chr_{}_data.csv'.format(ch))

stat = {
    'watterson': {},
    'n_mut': {},
    'n_non_na': {},
    'sample': {},
}

t1 = time.time()
for w in range(n_win):
    sample_lst = {}
    sample_str = {}
    for k, v in seq.items():
        s = v[w*w_size:(w+1)*w_size]
        sample_lst[k] = list(s)
        sample_str[k] = str(s)
    sample_lst = pd.DataFrame(sample_lst).T
    sample_lst = seqtools.drop_na_seq(sample_lst)
    sample_str = pd.Series(sample_str).loc[sample_lst.index]

    sample_lst_ref = pd.DataFrame(
        {'ref': list(seq_ref[w*w_size:(w+1)*w_size])}).T
    sample_lst_ref[sample_lst_ref == 'N'] = np.nan

    stat['watterson'][w] = seqtools.watterson(sample_lst)
    stat['n_mut'][w] = seqtools.n_mutations(sample_lst, sample_lst_ref)
    stat['n_non_na'][w] = sample_lst.shape[0]
    stat['sample'][w] = seqtools.encode_sample(
        sample_str, pad_with_nan=True, sample_size=n_seq)

for k, v in stat.items():
    if k in ['sample']:
        pd.DataFrame(v).T.to_csv('chr_{ch}_{k}.csv'.format(ch=ch, k=k))
    else:
        pd.Series(v).to_csv('chr_{ch}_{k}.csv'.format(ch=ch, k=k))

t2 = time.time()

with open('runtime_seq2stat_{}.txt'.format(ch), 'w') as f:
    f.write('{:0.0f}\n'.format(t2-t1))
