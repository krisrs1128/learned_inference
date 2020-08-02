#!/bin/bash
cd /home/kris/
source .env
mkdir $DATA_DIR
touch $DATA_DIR/test1.out
touch $_CONDOR_SCRATCH_DIR/test2.out
mkdir $_CONDOR_SCRATCH_DIR/data
touch $_CONDOR_SCRATCH_DIR/data/test3.out
