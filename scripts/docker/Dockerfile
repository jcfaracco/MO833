FROM ubuntu:19.04

RUN apt-get update
RUN apt-get install apt-utils openssh-client python3-pip -y

RUN pip3 install boto3 boto awscli
RUN pip3 install --upgrade requests

RUN apt-get install ansible jq -y

RUN ssh-keygen -t rsa -b 1024 -N "" -f /root/.ssh/id_rsa
RUN cat /root/.ssh/id_rsa.pub > /root/.ssh/authorized_keys

COPY data/credentials /root/.aws/

RUN mkdir /python
RUN mkdir /ansible
