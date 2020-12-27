#!/usr/bin/env bash

# unzip and clone
tar -zxvf stability_data.tar.gz
git clone https://github.com/krisrs1128/learned_inference.git
source learned_inference/.env

# prepare patches, taking care of R's 1 indexing
export B=${1}
((B++))
Rscript -e "rmarkdown::render('learned_inference/inference/vignettes/prepare_mibi.Rmd', params = list(j = ${B}, data_dir='../../../stability_data/tnbc/'))"
mv stability_data/tnbc/tiles/y.csv stability_data/tnbc/tiles/y_${B}.csv
cd stability_data/tnbc/
tar -zcvf tiles_${1}.tar.gz tiles/
mv tiles_${1}.tar.gz $_CONDOR_SCRATCH_DIR/
