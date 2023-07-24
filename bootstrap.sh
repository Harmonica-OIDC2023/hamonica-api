#!/bin/bash

# oci config permission setting
chmod 600 /root/.oci/*

# config oci fn
curl -LSs https://raw.githubusercontent.com/fnproject/cli/master/install | sh

# api server start
cd /app && python3 -m uvicorn app.main:app --reload --host="0.0.0.0" --port=80