#!/bin/bash
cd /home/kris/
source .env
touch $DATA_DIR/test1.out
touch $_CONDOR_SCRATCH_DIR/test2.out
mkdir $_CONDOR_SCRATCH_DIR
touch $_CONDOR_SCRATCH_DIR/test3.out
