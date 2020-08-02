#!/bin/bash
cd /home/kris/
source .env
mkdir $DATA_DIR
touch $DATA_DIR/test1.out
echo ${1}
echo $ROOT_DIR
cd $ROOT_DIR/learning/
python3 test_condor.py -b 10
touch pt1.out
python3 -m test_condor -b 10
touch pt2.out
python3 -m test_condor -b ${1}
touch pt3.out
