#!/usr/bin/env python3

from seqstats import main
import sys
from my_io import run

if __name__ == '__main__':
    var = {
        'ch': sys.argv[1],
        'block': 'seqstat',
        'n_core': 1,
        'fun': main,
    }
    run(var)
