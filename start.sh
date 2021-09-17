#!/bin/bash
app="autoinstall"
docker build -t ${app} .
docker run -d -it -p 127.0.0.1:56733:80 --restart unless-stopped --name=${app} \
--mount type=bind,source=/var/www/install,target=/app \
--mount type=bind,source=/srv/tftp,target=/srv/tftp \
--mount type=bind,source=/etc/dhcp/hosts,target=/srv/hosts \
${app}
