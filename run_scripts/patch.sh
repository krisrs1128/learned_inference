#!/usr/bin/env bash

# unzip and clone
tar -zxvf tnbc_raw.tar.gz
git clone https://github.com/krisrs1128/learned_inference.git
source learned_inference/.env

# prepare patches, keeping in mind that R is 1 indexed
((B++))
Rscript -e "rmarkdown::render('learned_inference/inference/vignettes/prepare_mibi.Rmd', params = list(j = ${B}, data_dir='../../../tnbc_raw/', out_dir='../../../stability_data'))"
mv stability_data/tiles/y.csv stability_data/tiles/y_${B}.csv
tar -zcvf stability_data_${B}.tar.gz stability_data
mv stability_data_${B}.tar.gz $_CONDOR_SCRATCH_DIR/
