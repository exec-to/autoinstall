#!/bin/bash
app="autoinstall"
docker build -t ${app} .
docker run -d -it -p 127.0.0.1:56733:80 --name=${app} \
--mount type=bind,source=/var/www/install,target=/app \
--mount type=bind,source=/opt/autoinst,target=/opt/autoinst \
--mount type=bind,source=/srv/tftp,target=/srv/tftp \
${app}
