FROM bioconductor/bioconductor_docker:devel
WORKDIR /home/rstudio
COPY --chown=rstudio:rstudio . /home/rstudio/

WORKDIR /home/rstudio/inference/
RUN apt-get update
RUN apt-get install -y libglpk-dev
RUN apt-get install -y libgdal-dev libproj-dev
RUN apt-get install -y software-properties-common

# install python
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN apt-get install -y python3.7
RUN apt-get install -y libpython3.7-dev
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-venv python3-virtualenv

# setup R package
RUN Rscript -e "install.packages('remotes')"
RUN Rscript -e "remotes::install_deps(dependencies = TRUE)"

WORKDIR /home/rstudio/learning/
RUN pip3 install -r requirements.txt