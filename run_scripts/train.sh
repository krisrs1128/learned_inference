#!/bin/bash
cd /home/kris/learning
echo ${0}
echo ${1}
python3 -m train -c ../conf/train.yaml -b ${1}
