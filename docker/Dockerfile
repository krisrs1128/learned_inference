FROM jupyter/datascience-notebook

USER root
RUN apt-get update
RUN apt-get install -y software-properties-common
RUN apt-get install -y apt-utils
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9
RUN add-apt-repository 'deb https://cloud.r-project.org/bin/linux/ubuntu focal-cran40/'
RUN apt-get update
RUN apt-get dist-upgrade
RUN apt-get install -y r-base r-base-core r-recommended
USER jovyan
RUN pip install osgeo
RUN Rscript -e "install.packages('sf', repos='http://cran.us.r-project.org')"