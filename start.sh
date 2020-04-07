#!/bin/bash
app="autoinstall"
docker build -t ${app} .
docker run -d -p 127.0.0.1:56733:80 \
  --name=${app} \
  -v $PWD:/app ${app}
