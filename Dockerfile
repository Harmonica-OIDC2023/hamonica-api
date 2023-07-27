FROM --platform=linux/amd64 ubuntu:22.04

USER root

# non interactive cmd
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get upgrade -y

RUN apt-get install -y sudo curl python3-pip apt-transport-https ca-certificates curl gnupg-agent software-properties-common

# install docker
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
RUN add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" -y
RUN apt-get update
RUN apt-get install -y docker-ce docker-ce-cli containerd.io

# install pip requirements
COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# api server
COPY ./ /app
EXPOSE 80

# bootstrap
COPY ./bootstrap.sh /app/bootstrap.sh
RUN chmod +x /app/bootstrap.sh
CMD ["/app/bootstrap.sh"]


