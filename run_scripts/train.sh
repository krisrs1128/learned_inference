#!/bin/bash

# unzip data and source environmental variables
tar -zxvf $_CONDOR_SCRATCH_DIR/stability_data.tar.gz
git clone https://github.com/krisrs1128/learned_inference.git
source learned_inference/.env
export BOOTSTRAP=${1}
export TRAIN_YAML=${3}

# trainig model
cd learned_inference/notebooks/
jupyter nbconvert --to=python model_training.ipynb
python3 -m model_training.py

# saving results
cd $_CONDOR_SCRATCH_DIR/
rm -rf $DATA_DIR/tiles/
export OUTNAME=$(basename ${3})_${1}.tar.gz
tar -zcvf ${OUTNAME} -C $DATA_DIR/ .
mv ${OUTNAME} /staging/ksankaran/
