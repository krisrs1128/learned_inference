#!/bin/bash
echo ${0}
echo ${1}
cd /home/kris/
source .env
cd learning
python3 -m train -c ../conf/train.yaml -b ${1}
