#!/bin/bash

# making sure to use appropriate python installation
tar -zxvf python38.tar.gz
tar -zxvf li-packages.tar.gz
export PATH=$PWD/python/bin:$PATH
export PYTHONPATH=$PWD/li-packages

# unzipping data and displaying parameters
tar -zxvf $_CONDOR_SCRATCH_DIR/stability_data.tar.gz
echo $0
echo $1
echo $2
echo $3

# training model
git clone https://github.com/krisrs1128/learned_inference.git
source learned_inference/.env
cd learned_inference/notebooks/

if [[ $3 == "cnn" ]]
then stuff
     python3 train_cnn.py
else
    python3 train_vae.py
fi

# saving results
cd $_CONDOR_SCRATCH_DIR/
tar -zcvf output_${2}_${1}.tar.gz $DATA_DIR/cnn/features/
