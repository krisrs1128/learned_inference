#!/bin/bash
cd /home/kris/
source .env
mkdir $DATA_DIR
touch $DATA_DIR/test1.out
echo ${1}
python3 test.py -b 10
touch pt1.out
cd $ROOT_DIR/learning/
python3 -m test -b 10
touch pt2.out
python3 -m test -b ${1}
touch pt3.out
