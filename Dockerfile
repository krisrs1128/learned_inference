FROM bioconductor/bioconductor_docker:devel
WORKDIR /home/rstudio
COPY --chown=rstudio:rstudio . /home/rstudio/

RUN cd /home/rstudio/inference/
RUN Rscript -e "remotes::install_github('r-hub/sysreqs')"
RUN sysreqs=$(Rscript -e "cat(sysreqs::sysreq_commands('DESCRIPTION'))")
RUN sudo -s eval "$sysreqs"
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
RUN apt-get update

# setup R package
RUN Rscript -e "install.packages('remotes')"
RUN Rscript -e "remotes::install_deps(dependencies = TRUE)"

RUN cd /home/rstudio/learning/
RUN pip3 install -r requirements.txt