"""Tools to work with samples of sequences."""

import pandas as pd
import numpy as np
from collections import Counter
import itertools
from partition import Partition


def drop_na_seq(sample):
    """
    Drops all sequences with NA SNPs.

    Args:
        sample (pd.DataFrame): with index sample ids and columns being SNP positions.

    Returns:
        New DataFrame without NA SNPs.
    """
    df = sample.copy()
    df[df == 'N'] = np.nan
    return df.dropna(axis=0, how='any')


def coverage(sample):
    """
    Coverage = number of non-NA sequences / total number.

    Args:
        sample (pd.DataFrame): with index sample ids and columns being SNP positions.

    Returns:
        coverage (float).
    """
    return drop_na_seq(sample).shape[0] * 1.0 / sample.shape[0]


def n_segregating_sites(sample):
    """
    Number of segregating sites.

    Args:
        sample (pd.DataFrame): with index sample ids and columns being SNP positions.

    Returns:
        (int)
    """
    if sample.shape[0] in [0, 1]:
        return np.nan
    n_unique = sample.apply(lambda snp_slice: len(np.unique(snp_slice)), axis=0)
    return len(n_unique[n_unique != 1])


def tajima(sample):
    """
    Tajima estimate of theta = average number of polymorphisms.
    This function is SLOW.

    Args:
        sample (pd.DataFrame): with index sample ids and columns being SNP positions.

    Returns:
        (float)
    """
    if sample.shape[0] in [0, 1]:
        return np.nan
    return np.mean([(a[1].ne(b[1])).sum() for a, b in itertools.combinations(sample.iterrows(), 2)])


def watterson(sample):
    """
    Watterson estimate of theta = number of segregating sites / harmonic number.

    Args:
        sample (pd.DataFrame): with index sample ids and columns being SNP positions.

    Returns:
        (float)
    """
    if sample.shape[0] in [0, 1]:
        return np.nan
    return n_segregating_sites(sample) / sum(1.0 / i for i in range(1, sample.shape[0]))


def n_mutations(sample, ref):
    """
    Number of mutations in a sample in comparison with reference sequence.

    Args:
        sample (pd.DataFrame): with index sample ids and columns being SNP positions.
        ref (pd.DataFrame) with only one index named 'ref' and columns being SNP positions.

    Returns:
        (int)
    """
    df = pd.concat([sample, ref])
    df = df.dropna(axis=1, how='any')
    if df.shape[0] in [0, 1]:
        return np.nan
    return sum([row.ne(df.loc['ref']).sum() for k, row in df.iterrows() if k != 'ref'])


def a_counts(sample):
    """
    Returns dict of a-counts {j: a_j}.

    Args:
        sample (pd.Series): with index sample ids and values being sequences.

    Returns:
        a-counts (dict)
    """
    counts = list(Counter(sample).values())
    return {j: counts.count(j) for j in range(1, len(sample)+1)}


def encode_sample(sample, pad_with_nan=False, sample_size=None):
    """
    Returns encoded sample: ['abc', 'xyz', 'abc'] -> [0, 1, 0] then shuffled.
    If pad_with_nan=True and sample_size=5 then [0, 1, 0, np.nan, np.nan].

    Args:
        sample (pd.Series): with index sample ids and values being sequences.
        pad_with_nan (bool).
        sample_size (int) desired sample size.

    Returns:
        (list)
    """
    d = Counter(sample)
    l = []
    for i, v in enumerate(d.values()):
        l.extend([i for _ in range(v)])
    np.random.shuffle(l)
    if pad_with_nan:
        return l + [np.nan] * (sample_size - len(l))
    return l


def n_counts(sample):
    """
    Returns n-counts.

    Args:
        sample (list of ints) encoded sample.

    Returns:
        (tuple)
    """
    # slow version
    # return tuple(sorted(Counter(sample).values(), reverse=True))
    counts = np.bincount(sample)
    counts[::-1].sort()
    counts = counts[counts > 0]
    return tuple(counts)


def sample2hist(sample, resample_size, n_itr):
    """
    Create a histogram of n-counts by
    resampling a given sample n_itr times
    drawing samples of size resample_size.

    Args:
        sample (list of ints) encoded sample.
        resample_size (int) size of a sample to do resampling.
        n_itr (int) number of iterations that builds the histogram.

    Returns:
        Histogram (pd.Series) with index being partitions.
    """
    part = Partition(resample_size)
    sample_non_na = np.round(pd.Series(sample).dropna()).astype(int)
    if len(sample_non_na) == 0:
        return pd.Series(np.nan, index=part.repr)
    h = pd.DataFrame(np.random.choice(sample_non_na, size=(n_itr, part.n), replace=True)).apply(n_counts, axis=1)
    h = h.value_counts() * 1.0 / n_itr
    return h.rename(part.map)
