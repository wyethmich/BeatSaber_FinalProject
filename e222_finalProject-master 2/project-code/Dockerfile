FROM ubuntu:18.04
MAINTAINER Eth N <30096019+eth-nn@users.noreply.github.com>

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y
RUN apt-get install -y apt-utils

RUN apt-get install -y build-essential libssl-dev

RUN apt-get install -y git-core
RUN apt-get install -y dnsutils
RUN apt-get install -y curl
RUN apt-get install -y python3.7

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.7 10
RUN update-alternatives --config python
RUN apt-get install -y python3.7-distutils
RUN apt-get install -y python3.7-dev


RUN curl -s https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python get-pip.py 

RUN pip install -U pip setuptools
RUN pip install psutil

RUN git clone https://github.com/eth-nn/beatsaver-Predictor

WORKDIR "/beatsaver-Predictor"
RUN git pull 

WORKDIR "/beatsaver-Predictor/project-code/scriptsPackage"
RUN pip install .

WORKDIR "/beatsaver-Predictor/project-code"

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["make", "start"]







