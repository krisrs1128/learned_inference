#!/usr/bin/env bash
tar -xzvf R402.tar.gz
export PATH=$PWD/R/bin:$PATH
export RHOME=$PWD/R
mkdir packages
export R_LIBS=$PWD/packages

Rscript -e "install.packages('devtools', repos='http://cran.us.r-project.org')"
Rscript -e "install.packages('dplyr', repos='http://cran.us.r-project.org')"
Rscript -e "install.packages('reshape2', repos='http://cran.us.r-project.org')"
Rscript -e "install.packages('ggplot2', repos='http://cran.us.r-project.org')"
Rscript -e "devtools::install_github('krisrs1128/learned_inference', subdir='inference')"
