# -*- coding: UTF-8 -*-
default = dict(
    BASE_PATH='',
)

auth = dict(
    key='token'
)

grub = {
    'setup_script': '/opt/autoinst/bin/setup.sh',
    'mkconfig-script': '/usr/sbin/grub-mkconfig',
    'config-directory':'/srv/tftp/boot/grub/conf.d',
    'temp-directory': '/opt/autoinst/var',
    'preseed-directory': '/opt/autoinst/preseed',
    'templates': {
        'local': {
           '0': '80_local'
        },
        'ubuntu': {
            '14': '90_ubuntu14',
            '16': '90_ubuntu16',
            '18': '90_ubuntu18'
        },
        'debian': {
            '8': '90_debian8',
            '9': '90_debian9',
            '10': '90_debian10'
        },
        'centos': {
            '7': '90_centos7',
            '8': '90_centos8'
        }
    }
}

os_list = [
    {'title': 'Ubuntu 14.04 LTS', 'os': 'ubuntu', 'osver': '14'},
    {'title': 'Ubuntu 16.04 LTS', 'os': 'ubuntu', 'osver': '16'},
    {'title': 'Ubuntu 18.04 LTS', 'os': 'ubuntu', 'osver': '18'},
    {'title': 'Debian 8', 'os': 'debian', 'osver': '8'},
    {'title': 'Debian 9', 'os': 'debian', 'osver': '9'},
    {'title': 'Debian 10', 'os': 'debian', 'osver': '10'},
    {'title': 'Centos 7', 'os': 'centos', 'osver': '7'},
    {'title': 'Centos 8', 'os': 'centos', 'osver': '8'}
]

local_networks = {
    '192.168.80.0/22': {'gateway': '192.168.80.1', 'netmask': '255.255.252.0'},
    '192.168.1.0/24': {'gateway': '192.168.1.1', 'netmask': '255.255.255.0'}
}

database = dict(
    user='ai',
    passwd='pass',
    host='local',
    port='3306',
    db='appdb'
)

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    },
    'querykey': {
        'type': 'apiKey',
        'in': 'query',
        'name': 'token'
    }
}