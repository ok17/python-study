FROM python:3.6.1
MAINTAINER Osamu Kashimura

WORKDIR /var/www/html

RUN apt-get update \
    && apt-get install -y wget libfontconfig fonts-migmix

RUN pip install selenium beautifulsoup4 requests

RUN wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2 \
    && tar jxvf phantomjs-2.1.1-linux-x86_64.tar.bz2 \
    && cd phantomjs-2.1.1-linux-x86_64/bin/ \
    && cp phantomjs /usr/local/bin/




