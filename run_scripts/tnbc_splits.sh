#!/usr/bin/env bash

# unzip data
tar -zxvf $_CONDOR_SCRATCH_DIR/tnbc.tar.gz
git clone https://github.com/krisrs1128/learned_inference.git
source learned_inference/.env_tnbc

# make split and package up
cd learned_inference/notebooks/
jupyter nbconvert --to=python tnbc_splits.ipynb
python3 -m tnbc_splits
tar -zcvf tnbc_splits.tar.gz tnbc
