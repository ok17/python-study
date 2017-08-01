FROM python:3.6.1
MAINTAINER Osamu Kashimura

WORKDIR /var/www/html

RUN apt-get update \
    && apt-get install -y wget libfontconfig fonts-migmix

RUN pip install numpy scipy sklearn

CMD ["python", "-m", "http.server", "--cgi", "80"]



