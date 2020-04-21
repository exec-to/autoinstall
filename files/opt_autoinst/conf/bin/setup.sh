#!/bin/bash
# DO NOT RUN ON HOST SERVER

GRUB_DIR="/etc/grub.d"
TPL_DIR="/opt/autoinst/template"
CONF_FILE=$1

/bin/rm -f ${GRUB_DIR}/80_*
/bin/rm -f ${GRUB_DIR}/90_*
cp -f ${TPL_DIR}/${CONF_FILE} ${GRUB_DIR}/${CONF_FILE}

