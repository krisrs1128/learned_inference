#!/usr/bin/env bash

tar -zxvf tnbc.tar.gz
tar -zxvf learned_inference.tar.gz
which python3
which python

cd learned_inference/inference/vignettes/
Rscript -e "rmarkdown::render('prepare_mibi.Rmd', params = list(j = ${1}, data_dir='../../../tnbc'))"
cd ../../../
mv tnbc/tiles/y.csv tnbc/tiles/y_${1}.csv
tar -zcvf tiles_${1}.tar.gz tnbc/tiles/
