#!/bin/bash
tar -zxvf $_CONDOR_SCRATCH_DIR/data.tar.gz
cd /home/kris/
source .env
cd learning
python3 -m bootstrap -c ../conf/train.yaml
python3 -m train -c ../conf/train.yaml -b ${1}
