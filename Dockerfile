FROM ubuntu:latest
WORKDIR /temp
RUN apt-get update
RUN apt-get install -y python3.7
RUN apt-get install -y curl
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -
RUN apt-get install -y nodejs
RUN apt-get install -y python3-lxml
RUN apt-get install -y python3-pip
RUN mkdir demo
COPY /demo /temp/demo
RUN cd demo
RUN npm install -g serve
ENV PYTHON_PACKAGES="\
	bson \
	flask \
	flask_cors \
	gevent \
	pymongo \
 	werkzeug \
        nltk \
        pytz \
        lxml \
"
RUN pip3 install --no-cache-dir $PYTHON_PACKAGES
RUN cd ..
COPY app.py app.py
COPY utils.py utils.py
COPY lauch.sh lauch.sh
EXPOSE 3000
EXPOSE 8003
CMD ./lauch.sh
