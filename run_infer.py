#!/usr/bin/env python3

from infer import main
import sys
from my_io import run

if __name__ == '__main__':
    var = {
        'ch': sys.argv[1],
        'n_core': 1,
        'fun': main,
        'prior': 'n',  # 'n' for normal and 'u' for uniform
        'is_neutral': True,
    }
    var['block'] = 'post_idx_{prior}{postfix}'.format(**var)
    run(var)
