#!/bin/bash
tar -zxvf $_CONDOR_SCRATCH_DIR/data.tar.gz
cd /home/kris/
source .env
cd learning
python3 -m train -c ../conf/fine_tuning/start_10.yaml -b ${1}
cd $_CONDOR_SCRATCH_DIR/
tar -zcvf data_output_${2}_${1}.tar.gz $DATA_DIR/runs/
