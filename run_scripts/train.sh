#!/bin/bash
tar -zxvf $_CONDOR_SCRATCH_DIR/data.tar.gz
cd $HOME
source .env
cd $ROOT_DIR/learning
echo $DATA_DIR
echo "parameters"
echo ${1}
echo ${2}
echo ${3}
ls -R
pwd
python3 -m bootstrap -c ${1}
ls -R $DATA_DIR
python3 -m train -c ${1} -b ${2}
ls -R $DATA_DIR
python3 -m features -c ${1} -m **/${2}/model_final.pt
ls -R $DATA_DIR

cd $_CONDOR_SCRATCH_DIR/
tar -zcvf data_output_${3}_${2}.tar.gz $DATA_DIR/features/
tar -zcvf data_models_${3}_${2}.tar.gz $DATA_DIR/runs/vae_boot/
