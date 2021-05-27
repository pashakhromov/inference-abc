import pandas as pd
import numpy as np
import os
import time
import sys
from my_io import get_path, read_df


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
    chunk = int(args['chunk'])
    n_chunk = int(args['n_chunk'])
    args['postfix'] = '_neutral' if args['is_neutral'] else ''
    path = get_path()

    stat_sim = pd.read_csv(os.path.join(path['sim'], 'stat_sim_{prior}{postfix}.csv'.format(**args)), **read_df)
    if n_chunk:
        n = stat_sim.shape[0]
        dn = n // n_chunk
        n1 = chunk * dn
        n2 = min(n1 + dn, n)
        stat_sim = stat_sim.loc[slice(n1, n2), :]

    idx_non_conv = stat_sim[stat_sim.isnull().any(axis=1)].index
    stat_sim = stat_sim.drop(idx_non_conv, axis=0)

    stat_obs = pd.read_csv(os.path.join(path['in'], 'chr_{ch}_hist.csv'.format(**args)), **read_df)
    stat_obs = stat_obs.astype(float)
    post_idx = stat_obs.apply(lambda x: get_post_idx(x, stat_sim, rho2_metric=args['rho2_metric']), axis=1)
    return {'post_idx_{prior}{postfix}'.format(**args): post_idx}


if __name__ == "__main__":
    pass
