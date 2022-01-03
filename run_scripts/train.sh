#!/bin/bash

# unzip data and source environmental variables
tar -zxvf stability_data_tnbc.tar.gz
tar -zxvf stability_data_sim.tar.gz
git clone https://github.com/krisrs1128/learned_inference.git
source learned_inference/.env

# trainig model
cd learned_inference/notebooks/
jupyter nbconvert --to=python model_training.ipynb
python3 -m model_training

# saving results
cd $DATA_DIR
rm -rf $DATA_DIR/tiles/
rm -rf $DATA_DIR/tnbc/
export OUTNAME=$(basename ${TRAIN_YAML})_${BOOTSTRAP}.tar.gz
tar -zcvf $OUTNAME -C $DATA_DIR/ .
mv $OUTNAME $_CONDOR_SCRATCH_DIR
