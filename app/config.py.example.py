# -*- coding: UTF-8 -*-
default = dict(
    BASE_PATH='',
)

auth = dict(
    key='token'
)

utils = {
    'config-directory':'/srv/tftp/boot/conf.d',
    'boot_url': 'tftp://10.0.222.1',
    'preseed-directory': '/opt/autoinst/preseed'
}

templates = dict(
    local_0=['#!ipxe\n', 'exit\n'],
    ubuntu_14=[
        '#!ipxe\n',
        'set boot-url __boot_url__\n',
        'set base-url /images/ubuntu/14/amd64\n',
        'kernel ${base-url}/linux auto=true priority=critical url=__boot_url__/boot/conf.d/s__srv_name__/s__srv_name__.seed --- quiet\n',
        'initrd ${base-url}/initrd.gz\n',
        'boot\n'
    ],
    ubuntu_16=[
        '#!ipxe\n',
        'set boot-url __boot_url__\n',
        'set base-url /images/ubuntu/16/amd64\n',
        'kernel ${base-url}/linux auto=true priority=critical url=__boot_url__/boot/conf.d/s__srv_name__/s__srv_name__.seed --- quiet\n',
        'initrd ${base-url}/initrd.gz\n',
        'boot\n'
    ],
    ubuntu_18=[
        '#!ipxe\n',
        'set boot-url __boot_url__\n',
        'set base-url /images/ubuntu/18/amd64\n',
        'kernel ${base-url}/linux auto=true priority=critical url=__boot_url__/boot/conf.d/s__srv_name__/s__srv_name__.seed --- quiet\n',
        'initrd ${base-url}/initrd.gz\n',
        'boot\n'
    ],
    debian_8=[
        '#!ipxe\n',
        'set boot-url __boot_url__\n',
        'set base-url /images/debian/8/amd64\n',
        'kernel ${base-url}/linux auto=true priority=critical url=__boot_url__/boot/conf.d/s__srv_name__/s__srv_name__.seed --- quiet\n',
        'initrd ${base-url}/initrd.gz\n',
        'boot\n'
    ],
    debian_9=[
        '#!ipxe\n',
        'set boot-url __boot_url__\n',
        'set base-url /images/debian/9/amd64\n',
        'kernel ${base-url}/linux auto=true priority=critical url=__boot_url__/boot/conf.d/s__srv_name__/s__srv_name__.seed --- quiet\n',
        'initrd ${base-url}/initrd.gz\n',
        'boot\n'
    ],
    debian_10=[
        '#!ipxe\n',
        'set boot-url __boot_url__\n',
        'set base-url /images/debian/10/amd64\n',
        'kernel ${base-url}/linux auto=true priority=critical url=__boot_url__/boot/conf.d/s__srv_name__/s__srv_name__.seed --- quiet\n',
        'initrd ${base-url}/initrd.gz\n',
        'boot\n'
    ],
    centos_7=[
        '#!ipxe\n',
        'set boot-url __boot_url__\n',
        'set base-url /images/centos/7/amd64\n',
        'kernel ${base-url}/vmlinuz inst.ks=__boot_url__/boot/conf.d/s__srv_name__/s__srv_name__.seed\n',
        'initrd ${base-url}/initrd.img\n',
        'boot\n'
    ],
    centos_8=[
        '#!ipxe\n',
        'set boot-url __boot_url__\n',
        'set base-url /images/centos/8/amd64\n',
        'kernel ${base-url}/vmlinuz inst.ks=__boot_url__/boot/conf.d/s__srv_name__/s__srv_name__.seed\n',
        'initrd ${base-url}/initrd.img\n',
        'boot\n'
    ],
)


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