#!/bin/bash
cd /home/kris/
source .env
mkdir $DATA_DIR
touch $DATA_DIR/test1.out
echo ${1}
echo $ROOT_DIR
echo $DATA_DIR
cd $ROOT_DIR/run_scripts/
python3 $ROOT_DIR/run_scripts/test_condor.py -b 10 -f $DATA_DIR
touch ${DATA_DIR}/pt1.out
python3 -m test_condor -b 10 -f $DATA_DIR
touch ${DATA_DIR}/pt2.out
python3 -m test_condor -b ${1} -f $DATA_DIR
touch ${DATA_DIR}/pt3.out
tar -zcvf data_small.tar.gz ${DATA_DIR}
