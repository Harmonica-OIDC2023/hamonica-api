FROM --platform=linux/amd64 ubuntu:22.04

USER root

RUN apt-get update
RUN apt-get upgrade -y

RUN apt-get install -y sudo curl python3-pip

# install pip requirements
COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# api server
COPY ./app /app/app
EXPOSE 80

# bootstrap
COPY ./bootstrap.sh /app/bootstrap.sh
RUN chmod +x /app/bootstrap.sh
CMD ["/app/bootstrap.sh"]


