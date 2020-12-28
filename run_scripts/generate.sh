#!/usr/bin/env bash

git clone https://github.com/krisrs1128/learned_inference.git
source learned_inference/.env

# generate raw tiles
Rscript -e "rmarkdown::render('learned_inference/inference/vignettes/generate.Rmd')"
mkdir stability_data
mv tiles stability_data/

# randomly assign to train / dev / test
cd learned_inference/notebooks
jupyter nbconvert --to=python save_splits.ipynb
python3 -m save_splits

# pass to output
cd $_CONDOR_SCRATCH_DIR
tar -zcvf stability_data.tar.gz stability_data.tar.gz
