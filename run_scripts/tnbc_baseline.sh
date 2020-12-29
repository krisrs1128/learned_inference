#!/usr/bin/env bash

# unzip data and source environmental variables
tar -zxvf stability_data.tar.gz
git clone https://github.com/krisrs1128/learned_inference.git
source learned_inference/.env

# run baseline
cd learned_inference/notebooks/
jupyter nbconvert --to=python tnbc_baseline.ipynb
python3 -m tnbc_baseline
cp $DATA_DIR/baseline.json $_CONDOR_SCRATCH_DIR/
