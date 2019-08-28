#!/usr/bin/env bash
python3 infer_2L.py &
python3 infer_2R_1.py &
python3 infer_2R_2.py &
python3 infer_3L.py &
python3 infer_3R.py &
python3 infer_X.py &