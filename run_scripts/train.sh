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
python3 train.py --train_yaml ${3} --bootstrap ${1}

# saving results
cd $_CONDOR_SCRATCH_DIR/
rm -rf $DATA_DIR/tiles/
export OUTNAME=$(basename ${3}).tar.gz
tar -zcvf ${OUTNAME} -C $DATA_DIR/ .
smbclient -k //research.drive.wisc.edu/ksankaran -c "put ${OUTNAME}"
