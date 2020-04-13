FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7
RUN apk --update add bash vim grub grub-dev 
RUN /bin/rm -f /etc/grub.d/*
RUN /bin/mv /usr/sbin/grub-probe /usr/sbin/grub-probe_bak
COPY ./grub-probe /usr/sbin/grub-probe 
COPY ./requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt
