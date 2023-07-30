#!/bin/bash

# oci config permission setting
chmod 600 /root/.oci/*

# config oci fn
curl -LSs https://raw.githubusercontent.com/fnproject/cli/master/install | sh

# config oci docker login
docker login -u 'idhxkx7uajar/ryann3@sookmyung.ac.kr' iad.ocir.io -p $DOCKER_PWD

# config kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/arm64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# func permission setting
curl -Lo knative_func  "https://github.com/knative/func/releases/download/knative-v1.11.0/func_linux_arm64"
mv knative_func /usr/local/bin/func
chmod +x /usr/local/bin/func

# api server start
cd /app && python3 -m uvicorn app.main:app --reload --host="0.0.0.0" --port=80