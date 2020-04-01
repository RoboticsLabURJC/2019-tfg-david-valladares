FROM arm32v7/debian:stretch-slim

#TAG arm32v7/ofuscacion

SHELL ["/bin/bash", "-c"]

COPY qemu-arm-static /usr/bin

RUN apt-get update 
RUN apt-get install -y python3-pip python3-dev 
RUN cd /usr/local/bin 
RUN ln -s /usr/bin/python3 python 
RUN pip3 install --upgrade pip 
RUN pip install pyarmor
RUN pyarmor

ARG GID=555

RUN useradd -ms /bin/bash jderobot
RUN groupadd -g $GID obfuscate
RUN usermod -g obfuscate jderobot
RUN usermod -a -G jderobot jderobot
USER jderobot

## All commands launch after this will be launch as jderobot ##
WORKDIR /home/jderobot



