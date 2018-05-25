FROM kbase/kbase:sdkbase2.latest
MAINTAINER KBase Developer
# -----------------------------------------
# In this section, you can install any system dependencies required
# to run your App.  For instance, you could place an apt-get update or
# install line here, a git checkout to download code, or run any other
# installation scripts.

# RUN apt-get update

# Here we install a python coverage tool and an
# https library that is out of date in the base image.

RUN pip install coverage

# -----------------------------------------

# download prepDE script
RUN cd /kb/dev_container/modules && \
    mkdir prepDE && cd prepDE && \
    wget http://ccb.jhu.edu/software/stringtie/dl/prepDE.py &&\
    mkdir /kb/deployment/bin/prepDE && \
    cp -R prepDE.py /kb/deployment/bin/prepDE/prepDE.py && \
    chmod 777 /kb/deployment/bin/prepDE/prepDE.py

# -----------------------------------------

# install R dependency
RUN sudo add-apt-repository ppa:marutter/rrutter3.5 -y && \
    sudo apt-get update && \
    yes '' | sudo apt-get -y install r-base && \
    yes '' | sudo apt-get -y install r-base-dev && \
    wget "https://bioconductor.org/biocLite.R" -O /kb/deployment/bin/prepDE/biocLite.R

RUN echo 'update.packages(ask = FALSE, checkBuilt = TRUE)\ninstall.packages(c("getopt"), lib="/kb/deployment/bin/prepDE", repos="http://cran.us.r-project.org", dependencies=TRUE)\nremove.packages("BiocInstaller", lib=.libPaths())\nsource("http://bioconductor.org/biocLite.R")\nbiocLite("Biobase")\nsource("http://bioconductor.org/biocLite.R")\nbiocLite("DESeq2")' > /kb/deployment/bin/prepDE/packages.R && \
    Rscript /kb/deployment/bin/prepDE/packages.R

# -----------------------------------------

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
