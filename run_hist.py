#!/usr/bin/env python3

import sys
from hist import main
from my_io import run

if __name__ == '__main__':
    var = {
        'ch': sys.argv[1],
        'block': 'hist',
        'n_core': 1,
        'fun': main,
    }
    run(var)
