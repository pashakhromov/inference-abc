import pandas as pd
from seqtools import sample2hist
import os
from my_io import get_path, read_df


def main(args):
    ch = args['ch']
    chunk = int(args['chunk'])
    n_chunk = int(args['n_chunk'])

    path = get_path()

    n_itr = 10_000
    resample_size = 5

    sample = pd.read_csv(os.path.join(path['in'], 'chr_{}_sample.csv'.format(ch)), **read_df)
    if n_chunk:
        n = sample.shape[0]
        dn = n // n_chunk
        n1 = chunk * dn
        n2 = min(n1 + dn, n)
        sample = sample.loc[slice(n1, n2), :]

    hist = sample.apply(lambda x: sample2hist(x, resample_size=resample_size, n_itr=n_itr), axis=1).fillna(0)
    return {'hist': hist}


if __name__ == '__main__':
    pass
