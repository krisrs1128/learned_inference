#!/usr/bin/env bash

tar -zxvf stability_data.tar.gz
tar -zxvf stability_outputs.tar.gz

git clone https://github.com/krisrs1128/learned_inference.git
source learned_inference/.env
Rscript -e "rmarkdown::render('learned_inference/inference/vignettes/stability.Rmd', params = list(data_dir = '../../../stability_outputs/', layer = '${LAYER}', model_prefix = '${PREFIX}', sca = ${SCA}, save_dir = '../../../figures', tiles_dir = '../../../stability_data/'))"

tar -zcvf figures_$PREFIX_$LAYER_$SCA.tar.gz figures/
