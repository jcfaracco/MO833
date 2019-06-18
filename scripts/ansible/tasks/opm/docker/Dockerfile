FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install software-properties-common -y

RUN apt-add-repository ppa:opm/ppa -y
RUN apt-get update

RUN apt-get install mpi-default-bin libopm-simulators-bin git -y

RUN echo 'LANG="en_US.UTF-8"' >> ~/.bash_profile
RUN echo 'export LANG' >> ~/.bash_profile
RUN echo 'LC_ALL="en_US.UTF-8"' >> ~/.bash_profile
RUN echo 'export LC_ALL' >> ~/.bash_profile

RUN mkdir /opm
WORKDIR /opm

RUN git clone https://github.com/OPM/opm-data.git
