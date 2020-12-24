FROM ubuntu:20.04

RUN apt-get update
RUN apt-get install -y software-properties-common
RUN apt-get install -y dirmngr gnupg apt-transport-https ca-certificates software-properties-common
RUN  apt-get install -y libudunits2-dev libgit2-dev
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9
RUN add-apt-repository 'deb https://cloud.r-project.org/bin/linux/ubuntu focal-cran40/'
RUN apt-get install -y r-base
RUN apt-get install -y libgdal-dev gdal-bin
RUN Rscript -e "install.packages('sf', repos='http://cran.us.r-project.org')"
RUN Rscript -e "install.packages('devtools', repos='http://cran.us.r-project.org')"
RUN Rscript -e "install.packages('BiocManager', repos='http://cran.us.r-project.org')"
RUN Rscript -e "BiocManager::install('SingleCellExperiment')"
RUN Rscript -e "devtools::install_github('krisrs1128/learned_inference/inference')"
RUN apt-get install -y pandoc
RUN Rscript -e "install.packages('rmarkdown', repos='http://cran.us.r-project.org')"
RUN Rscript -e "install.packages('stringr', repos='http://cran.us.r-project.org')"