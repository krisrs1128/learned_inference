FROM ubuntu:20.04

RUN apt-get update
RUN apt-get install -y software-properties-common

# installing R
RUN apt-get install -y dirmngr gnupg apt-transport-https ca-certificates software-properties-common
RUN  apt-get install -y libudunits2-dev libgit2-dev
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9
RUN add-apt-repository 'deb https://cloud.r-project.org/bin/linux/ubuntu focal-cran40/'
RUN apt-get install -y r-base

# programs needed for rmarkdown, rgdal, and epca
RUN apt-get install -y pandoc
RUN apt-get install -y libgdal-dev gdal-bin
RUN apt-get install -y libx11-dev 

# R packages used in this work
RUN Rscript -e "install.packages('devtools', repos='http://cran.us.r-project.org')"
RUN Rscript -e "install.packages('ggplot2', repos='http://cran.us.r-project.org')"
RUN Rscript -e "install.packages('purrr', repos='http://cran.us.r-project.org')"
RUN Rscript -e "install.packages('rgdal', repos='http://cran.us.r-project.org')"
RUN Rscript -e "install.packages('rmarkdown', repos='http://cran.us.r-project.org')"
RUN Rscript -e "install.packages('stars', repos='http://cran.us.r-project.org')"
RUN Rscript -e "install.packages('stringr', repos='http://cran.us.r-project.org')"
RUN Rscript -e "install.packages('yaml', repos='http://cran.us.r-project.org')"
RUN Rscript -e "install.packages('BiocManager', repos='http://cran.us.r-project.org')"
RUN Rscript -e "BiocManager::install('SingleCellExperiment')"
RUN Rscript -e "devtools::install_github('krisrs1128/learned_inference/inference')"
RUN Rscript -e "devtools::install_github('fchen365/epca')"

# installing python
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN apt-get install -y python3.8 python3-pip
RUN pip3 install numpy jupyterlab

# our stability package
RUN apt-get install -y git
RUN git clone https://github.com/krisrs1128/learned_inference.git
RUN pip3 install learned_inference/stability