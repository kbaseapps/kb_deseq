FROM kbase/sdkbase2:python
MAINTAINER KBase Developer
# -----------------------------------------
# In this section, you can install any system dependencies required
# to run your App.  For instance, you could place an apt-get update or
# install line here, a git checkout to download code, or run any other
# installation scripts.
# -----------------------------------------

# install R dependencies
RUN conda install -y r-essentials r-base r-xml r-rcurl
RUN apt-get update &&\
    apt-get install -y g++
RUN R -q -e 'install.packages("getopt",  repos="http://cran.us.r-project.org")' && \
    R -q -e 'if (!require("getopt")) {quit(status=1)}'
RUN R -q -e 'install.packages("BiocManager", repos="http://cran.us.r-project.org")' && \
    R -q -e 'BiocManager::install("DESeq2", ask=FALSE)' && \
    R -q -e 'if (!require("DESeq2")) {quit(status=1)}'

RUN pip install --upgrade pip \
    && python --version

RUN pip install coverage==5.5 && \
    pip install requests==2.26.0 && \
    pip install nose==1.3.7
# -----------------------------------------

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
