#!/bin/bash
cd ../learning
python3 -m train -c ../conf/train.yaml -b ${1}
