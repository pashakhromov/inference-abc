#!/usr/bin/env python3

import os
import socket


def get_path():
    if socket.gethostname() == 'laptopus':
        return {
            'sim': '/home/pasha/Desktop/phd/sim_data',
            'in': '/home/pasha/Desktop/phd/chr_data',
            'out': '/home/pasha/Desktop/phd/chr_data/test',
        }
    else:
        return {
            'sim': '/home/pasha/sim_data',
            'in': '/home/pasha/chr_data',
            'out': '/home/pasha/chr_data',
        }


read_series = {
    'index_col': 0,
    'header': None,
    'squeeze': True,
}

read_df = {
    'index_col': 0,
}

if __name__ == '__main__':
    pass
