#!/usr/bin/env bash

tar -zxvf stability_outputs.tar.gz

git clone https://github.com/krisrs1128/learned_inference.git
git clone https://github.com/krisrs1128/learned_inference.git
source learned_inference/.env
Rscript -e "rmarkdown::render('learned_inference/inference/vignettes/procrustes.Rmd', params = list(data_dir = '../../../stability_outputs/', layer = 'linear', model_prefix = 'tnbc_cnn', sca = FALSE, save_dir = '../../../figures'))"
