import pandas as pd
import numpy as np
from collections import Counter
import itertools

def drop_na_seq(sample):
    """
    Drops all sequences with NA SNPs.

    Parameters:
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
    
    Parameters:
        sample (pd.DataFrame): with index sample ids and columns being SNP positions.
    
    Returns:
        coverage (float).
    """
    return drop_na_seq(sample).shape[0] * 1.0 / sample.shape[0]

def n_segregating_sites(sample):
    """
    Number of segregating sites.
    
    Parameters:
        sample (pd.DataFrame): with index sample ids and columns being SNP positions.
    
    Returns:
        (int)
    """
    n_unique = sample.apply(lambda snp_slice: len(np.unique(snp_slice)), axis=0)
    return len(n_unique[n_unique != 1])

def avg_n_poly(sample):
    """
    Average number of polymorphisms. This function is SLOW.
    
    Parameters:
        sample (pd.DataFrame): with index sample ids and columns being SNP positions.
    
    Returns:
        (float)
    """
    return np.mean([(a[1] != b[1]).sum() for a, b in itertools.combinations(sample.iterrows(), 2)])

def watterson(sample):
    """
    Watterson estimate of theta.
    
    Parameters:
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
    
    Parameters:
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
    
    Parameters:
        sample (pd.Series): with index sample ids and values being sequences.
    
    Returns:
        a-counts (dict)
    """
    counts = list(Counter(sample).values())
    return {j: counts.count(j) for j in range(1, len(sample)+1)}

def encode_sample(sample):
    """
    Returns encoded sample: ['abc', 'xyz', 'abc'] -> [0, 1, 0] then shuffled.
    
    Parameters:
        sample (pd.Series): with index sample ids and values being sequences.
    
    Returns:
        (list)
    """
    d = Counter(sample)
    l = []
    for i, v in enumerate(d.values()):
        l.extend([i for _ in range(v)])
    np.random.shuffle(l)
    return l
