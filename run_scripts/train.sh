#!/bin/bash

# making sure to use appropriate python installation
tar -zxvf python38.tar.gz
tar -zxvf li-packages.tar.gz
export PATH=$PWD/python/bin:$PATH
export PYTHONPATH=$PWD/li-packages

# unzipping data and displaying parameters
tar -zxvf $_CONDOR_SCRATCH_DIR/stability_data.tar.gz
source .env

# training model
git clone https://github.com/krisrs1128/learned_inference.git
cd learned_inference/notebooks/
python3 train_cnn.py

# saving results
cd $_CONDOR_SCRATCH_DIR/
tar -zcvf output_${2}_${3}.tar.gz $DATA_DIR/features/
