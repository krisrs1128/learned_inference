#!/bin/bash
tar -zxvf $_CONDOR_SCRATCH_DIR/data.tar.gz
cd $HOME
source .env
cd $ROOT_DIR/learning
echo "parameters"
echo ${1}
echo ${2}
echo ${3}
ls -R
pwd
python3 -m bootstrap -c ${1}
python3 -m train -c ${1} -b ${2}
python3 -m features -c ${1}

cd $_CONDOR_SCRATCH_DIR/
tar -zcvf data_output_${3}_${2}.tar.gz $DATA_DIR/features/
