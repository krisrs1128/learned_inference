#!/bin/bash
ls $HOME
cd $HOME
pwd
source .env
ls $ROOT_DIR
ls $DATA_DIR
cd $ROOT_DIR/learning
ls
pwd
python3 -m bootstrap -c ${1}
python3 -m train -c ${1} -b ${2}
python3 -m features -c ${1}

cd $_CONDOR_SCRATCH_DIR/
tar -zcvf data_output_${3}_${2}.tar.gz $DATA_DIR/features/
