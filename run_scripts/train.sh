#!/bin/bash

# making sure to use appropriate python installation
tar -zxvf python38.tar.gz
tar -zxvf li-packages.tar.gz
export PATH=$PWD/python/bin:$PATH
export PYTHONPATH=$PWD/packages

# unzipping data and displaying parameters
tar -zxvf $_CONDOR_SCRATCH_DIR/stability_data.tar.gz
cd $HOME
source .env
cd $ROOT_DIR/learning
echo $DATA_DIR
echo "parameters"
echo ${1}
echo ${2}
echo ${3}
ls -R
pwd


# training model
ipython -c "%run notebooks/train_cnn.ipynb"
ls -lsh .

# saving results
cd $_CONDOR_SCRATCH_DIR/
tar -zcvf output_${2}_${3}.tar.gz $DATA_DIR/features/
