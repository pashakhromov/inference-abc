import pandas as pd
import numpy as np
import os
import time

t1 = time.time()

ch = '2L'
prior = 'n'  # 'n' for normal and 'u' for uniform
n_sub = 1000

path = '/home/pasha/chr_data'

par_sim = pd.read_csv(os.path.join(path, 'par_sim_{}.csv'.format(prior)), index_col=0)
stat_sim = pd.read_csv(os.path.join(path, 'stat_sim_{}.csv'.format(prior)), index_col=0)

idx_non_conv = stat_sim[stat_sim.isnull().any(axis=1)].index
par_sim = par_sim.drop(idx_non_conv, axis=0)
stat_sim = stat_sim.drop(idx_non_conv, axis=0)

# stat_obs = pd.read_csv(os.path.join(data_path, 'hist_{}.csv'.format(ch)), index_col=0)
# stat_obs = stat_obs.loc[3000:3199, :]


def get_post_idx(stat_obs):
    n_top = 100

    if np.abs(stat_obs.iloc[-1] - 1.0) < 1e-9:
        return pd.Series(np.zeros(n_top))

    rho2 = ((stat_sim - stat_obs) ** 2 / stat_sim).sum(axis=1)
    idx = rho2.sort_values().iloc[:n_top].index
    return pd.Series(idx)


# #post_idx = stat_obs.apply(get_post_idx, axis=1)
# #post_idx.to_csv(os.path.join(data_path, 'post_idx_{}.csv'.format(ch)))
# write_header = True
# for stat_obs in pd.read_csv(os.path.join(path, 'chr_{}_hist.csv'.format(ch)), index_col=0, chunksize=1000):
#     stat_obs = stat_obs.astype(float)
#     post_idx = stat_obs.apply(get_post_idx, axis=1)
#     fname = os.path.join(path, 'chr_{}_post_idx.csv'.format(ch))
#     if write_header:
#         post_idx.to_csv(fname, mode='a', header=True)
#         write_header = False
#     else:
#         post_idx.to_csv(fname, mode='a', header=False)

stat_obs = pd.read_csv(os.path.join(path, 'chr_{}_hist.csv'.format(ch)), index_col=0)
if n_sub:
    stat_obs = stat_obs.iloc[:n_sub, :]
stat_obs = stat_obs.astype(float)
post_idx = stat_obs.apply(get_post_idx, axis=1)
post_idx.to_csv(os.path.join(path, 'chr_{}_post_idx.csv'.format(ch)))

t2 = time.time()
fname = os.path.join(path, 'infer_runtime_{}.txt'.format(ch))
with open(fname, 'w') as f:
    f.write('{:0.2f}\n'.format(t2-t1))
