#!/bin/bash
cd /home/kris/
source .env
mkdir $DATA_DIR
touch $DATA_DIR/test1.out
python3 -c 'print("Hi")'
