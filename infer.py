import pandas as pd
import numpy as np
import os
import time
import socket
import sys
from my_io import get_path, read_series, read_df


def get_post_idx(stat_obs, stat_sim, rho2_metric='chi2', n_top=100):
    eps = 1e-17

    if np.abs(stat_obs.iloc[-1] - 1.0) < eps or stat_obs.sum() < eps:
        return pd.Series([np.nan] * n_top)

    if rho2_metric == 'chi2':
        rho2 = ((stat_sim - stat_obs) ** 2 / stat_sim).sum(axis=1)
    if rho2_metric == 'eucl':
        rho2 = ((stat_sim - stat_obs) ** 2).sum(axis=1)
    idx = rho2.sort_values().iloc[:n_top].index
    return pd.Series(idx)


def main(args):
    args['postfix'] = '_neutral' if args['is_neutral'] else ''
    path = get_path()

    stat_sim = pd.read_csv(os.path.join(path['sim'], 'stat_sim_{prior}{postfix}.csv'.format(**args)), index_col=0)
    idx_non_conv = stat_sim[stat_sim.isnull().any(axis=1)].index
    stat_sim = stat_sim.drop(idx_non_conv, axis=0)

    print(args)
    print(path)
    print(stat_sim.shape)

    stat_obs = pd.read_csv(os.path.join(path['in'], 'chr_{ch}_hist.csv'.format(**args)), index_col=0)
    stat_obs = stat_obs.astype(float)
    stat_obs = stat_obs.iloc[:1000, :]
    post_idx = stat_obs.apply(lambda x: get_post_idx(x, stat_sim, rho2_metric=args['rho2_metric']), axis=1)
    fpath = os.path.join(path['out'], 'chr_{ch}_post_idx_{prior}{postfix}.csv'.format(**args))
    post_idx.to_csv(fpath)

    # c = 0
    # write_header = True
    # for stat_obs in pd.read_csv(os.path.join(path['in'], 'chr_{ch}_hist.csv'.format(**args)), index_col=0, chunksize=1000):
    #     stat_obs = stat_obs.astype(float)
    #     post_idx = stat_obs.apply(lambda x: get_post_idx(
    #         x, stat_sim, rho2_metric=args['rho2_metric']), axis=1)
    #     fpath = os.path.join(
    #         path['out'], 'chr_{ch}_post_idx_{prior}{postfix}.csv'.format(**args))
    #     if write_header:
    #         post_idx.to_csv(fpath, mode='a', header=True)
    #         write_header = False
    #     else:
    #         post_idx.to_csv(fpath, mode='a', header=False)

    #     c += 1
    #     if c > 0:
    #         break


if __name__ == "__main__":
    args = {
        'ch': sys.argv[1],
        'prior': sys.argv[2],
        'is_neutral': int(sys.argv[3]),
        'rho2_metric': sys.argv[4],
    }
    t1 = time.time()

    main(args)

    t2 = time.time()
    print('\nRuntime = {:0.2f} sec'.format(t2-t1))
    path = get_path()
    fpath = os.path.join(
        path['out'], 'chr_{ch}_infer_runtime_{prior}{postfix}.txt'.format(**args))
    with open(fpath, 'w') as f:
        f.write('{:0.2f}\n'.format(t2-t1))
