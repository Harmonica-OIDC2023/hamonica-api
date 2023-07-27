#!/bin/bash

# oci config permission setting
chmod 600 /root/.oci/*

# config oci fn
curl -LSs https://raw.githubusercontent.com/fnproject/cli/master/install | sh

# config oci docker login
docker login -u 'idhxkx7uajar/ryann3@sookmyung.ac.kr' iad.ocir.io -p $DOCKER_PWD

# api server start
cd /app && python3 -m uvicorn app.main:app --reload --host="0.0.0.0" --port=80