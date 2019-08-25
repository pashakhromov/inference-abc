import pandas as pd
from seqtools import sample2hist

import time
t1 = time.time()

ch = '2L'
n_itr = 10000
resample_size = 5
n_subset = 100

sample = pd.read_csv('/scratch/pnk16/abc/data/sample_{}.csv'.format(ch), index_col=0)

if n_subset:
    sample = sample.iloc[:n_subset, :]

hist = sample.apply(lambda x: sample2hist(x, resample_size=resample_size, n_itr=n_itr), axis=1)
hist.fillna(0).to_csv('hist_{}.csv'.format(ch))

t2 = time.time()
with open('time.txt', 'w') as f:
    f.write('{0.2f}'.format(t2-t1))