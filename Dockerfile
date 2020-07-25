FROM bioconductor/bioconductor_docker:devel
WORKDIR /home/rstudio
COPY --chown=rstudio:rstudio . /home/rstudio/

RUN Rscript -e "remotes::install_github('r-hub/sysreqs')"
RUN sysreqs=$(Rscript -e "cat(sysreqs::sysreq_commands('DESCRIPTION'))")
RUN sudo -s eval "$sysreqs"
RUN apt-get install -y libglpk-dev
RUN apt-get install -y libgdal-dev libproj-dev
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN apt-get install -y python3.7
RUN apt-get install -y libpython3.7-dev
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-venv python3-virtualenv
RUN apt-get update
RUN 
RUN options(repos = c(CRAN = "https://cran.r-project.org"))
RUN BiocManager::repositories()
RUN remotes::install_deps(dependencies = TRUE, repos = BiocManager::repositories())

RUN cd /home/rstudio/
RUN pip3 install -r requirements.txt