#!/usr/bin/env bash
#
# These are steps to run after submitting the interactive job,
#
# condor_submit -i intall_python.submit
#
# which let you use your python package on condor. The instructions are
# generally copied and pasted from https://chtc.cs.wisc.edu/python-jobs.shtml

tar -zxvf python38.tar.gz
export PATH=$PWD/python/bin:$PATH

mkdir li-packages
git clone https://github.com/krisrs1128/learned_inference.git
mv learned_inference li-packages/
python3 -m pip install --target=li-packages li-packages/learned_inference/stability/
tar -zcvf li-packages.tar.gz li-packages
