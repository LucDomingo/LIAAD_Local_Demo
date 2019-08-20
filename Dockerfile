FROM library/python:3.7.1-alpine

WORKDIR /workdir

RUN apk update && apk upgrade && \
    apk add --no-cache bash git openssh && \
    apk add build-base

RUN apk add bash
RUN apk add pcre-dev 
RUN pip install --upgrade pip
RUN apk add --update nodejs npm
RUN apk --update add --virtual scipy-runtime python py-pip \
    && apk add --virtual scipy-build \
        build-base python-dev openblas-dev freetype-dev pkgconfig gfortran \
    && ln -s /usr/include/locale.h /usr/include/xlocale.h \
    && pip install --no-cache-dir numpy \ 
    && pip install --no-cache-dir matplotlib \
    && pip install --no-cache-dir scipy \
    && apk del scipy-build \
    && apk add --virtual scipy-runtime \
        freetype libgfortran libgcc libpng  libstdc++ musl openblas tcl tk \
    && rm -rf /var/cache/apk/*

# Install python dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install git+https://github.com/LIAAD/py-pampo.git
RUN pip install git+https://github.com/LIAAD/TemporalSummarizationFramework


# Now install and build the demo
COPY demo/ demo/
RUN ./scripts/build_demo.py

COPY app.py app.py

EXPOSE 8000

CMD python app.py 