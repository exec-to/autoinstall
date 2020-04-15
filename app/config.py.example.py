# -*- coding: UTF-8 -*-
default = dict(
    BASE_PATH=''
)

auth = dict(
    client='mykey'
)

database = dict(
    user='user',
    passwd='pass',
    host='127.0.0.1',
    port='3306',
    db='dbname'
)

# grub['templates']['ubuntu']['16']
grub = {
    'setup_script': '/opt/autoinst/bin/setup.sh',
    'mkconfig-script': '/usr/sbin/grub-mkconfig',
    'config-directory':'/srv/tftp/boot/grub/conf.d',
    'temp-directory': '/opt/autoinst/var',
    'templates': {
        'local': {
           '0': '90_local'
        },
        'ubuntu': {
            '16': '90_ubuntu16'
        }
    }
}

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}