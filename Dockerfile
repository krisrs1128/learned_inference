FROM ubuntu:18.04
WORKDIR /home/kris
COPY . /home/kris/

RUN apt-get update
RUN apt-get install -y libglpk-dev libudunits2-dev
RUN apt-get install -y libgdal-dev libproj-dev
RUN apt-get install -y software-properties-common

# install python
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN apt-get install -y python3.7
RUN apt-get install -y libpython3.7-dev
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-venv python3-virtualenv

WORKDIR /home/kris/learning/
RUN pip3 install -r requirements.txt

# install R
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -y install tzdata
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9
RUN add-apt-repository 'deb https://cloud.r-project.org/bin/linux/ubuntu bionic-cran40/'
RUN apt-get update
RUN apt install -y r-base

# setup R package
WORKDIR /home/kris/inference/
RUN echo $(ls -1 /home/)
RUN echo $(ls -1 /home/kris/)
RUN echo $(ls -1 /home/kris/inference/)
RUN Rscript -e "install.packages('remotes')"
RUN Rscript -e "remotes::install_deps(dependencies = TRUE)"

WORKDIR /home/kris/learning/
