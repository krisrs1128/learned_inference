#!/bin/bash
tar -zxvf $_CONDOR_SCRATCH_DIR/data.tar.gz
cd $HOME
source .env
cd $ROOT_DIR/learning
python3 -m bootstrap -c ${1}
python3 -m train -c ${1} -b ${2}
python3 -m features -c ${1}

cd $_CONDOR_SCRATCH_DIR/
ls $DATA_DIR
tar -zcvf data_output_${3}_${2}.tar.gz $DATA_DIR/features/
