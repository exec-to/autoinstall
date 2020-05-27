# -*- coding: UTF-8 -*-
default = dict(
    BASE_PATH='',
)

auth = dict(
    key='token'
)


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

utils = {
    'config-directory':'/srv/tftp/boot/conf.d',
    'boot_host': '10.0.222.1',
    'boot_url': 'tftp://10.0.222.1',
    'preseed-directory': '/app/preseed'
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
    ubuntu_20=[
        '#!ipxe\n',
        'set boot-url __boot_url__\n',
        'set base-url /images/ubuntu/20/amd64\n',
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
    windows_std_2012r2_en=[
        '#!ipxe\n',
        'set boot-url __boot_url__\n',
        'kernel /boot/pxe/wimboot\n',
        'initrd /boot/conf.d/s__srv_name__/install.bat install.bat\n',
        'initrd /boot/pxe/winpeshl.ini winpeshl.ini\n',
        'initrd /images/windows/2012r2_en/amd64/boot/bcd BCD\n',
        'initrd /images/windows/2012r2_en/amd64/boot/boot.sdi boot.sdi\n',
        'initrd /images/windows/2012r2_en/amd64/sources/boot.wim boot.wim\n',
        'initrd http://install.adman.cloud/api/v1.0/install/prestart/__srv_name__?token=__token__ api\n',
        'boot\n'
    ],
    windows_dc_2012r2_en=[
        '#!ipxe\n',
        'set boot-url __boot_url__\n',
        'kernel /boot/pxe/wimboot\n',
        'initrd /boot/conf.d/s__srv_name__/install.bat install.bat\n',
        'initrd /boot/pxe/winpeshl.ini winpeshl.ini\n',
        'initrd /images/windows/2012r2_en/amd64/boot/bcd BCD\n',
        'initrd /images/windows/2012r2_en/amd64/boot/boot.sdi boot.sdi\n',
        'initrd /images/windows/2012r2_en/amd64/sources/boot.wim boot.wim\n',
        'initrd http://install.adman.cloud/api/v1.0/install/prestart/__srv_name__?token=__token__ api\n',
        'boot\n'
    ],
    windows_std_2012r2_ru=[
        '#!ipxe\n',
        'set boot-url __boot_url__\n',
        'kernel /boot/pxe/wimboot\n',
        'initrd /boot/conf.d/s__srv_name__/install.bat install.bat\n',
        'initrd /boot/pxe/winpeshl.ini winpeshl.ini\n',
        'initrd /images/windows/2012r2_ru/amd64/boot/bcd BCD\n',
        'initrd /images/windows/2012r2_ru/amd64/boot/boot.sdi boot.sdi\n',
        'initrd /images/windows/2012r2_ru/amd64/sources/boot.wim boot.wim\n',
        'initrd http://install.adman.cloud/api/v1.0/install/prestart/__srv_name__?token=__token__ api\n',
        'boot\n'
    ],
    windows_dc_2012r2_ru=[
        '#!ipxe\n',
        'set boot-url __boot_url__\n',
        'kernel /boot/pxe/wimboot\n',
        'initrd /boot/conf.d/s__srv_name__/install.bat install.bat\n',
        'initrd /boot/pxe/winpeshl.ini winpeshl.ini\n',
        'initrd /images/windows/2012r2_ru/amd64/boot/bcd BCD\n',
        'initrd /images/windows/2012r2_ru/amd64/boot/boot.sdi boot.sdi\n',
        'initrd /images/windows/2012r2_ru/amd64/sources/boot.wim boot.wim\n',
        'initrd http://install.adman.cloud/api/v1.0/install/prestart/__srv_name__?token=__token__ api\n',
        'boot\n'
    ],
    windows_std_2008r2_en=[
        '#!ipxe\n',
        'set boot-url __boot_url__\n',
        'kernel /boot/pxe/wimboot\n',
        'initrd /boot/conf.d/s__srv_name__/install.bat install.bat\n',
        'initrd /boot/pxe/winpeshl.ini winpeshl.ini\n',
        'initrd /images/windows/2008r2_en/amd64/boot/bcd BCD\n',
        'initrd /images/windows/2008r2_en/amd64/boot/boot.sdi boot.sdi\n',
        'initrd /images/windows/2008r2_en/amd64/sources/boot.wim boot.wim\n',
        'initrd http://install.adman.cloud/api/v1.0/install/prestart/__srv_name__?token=__token__ api\n',
        'boot\n'
    ],
    windows_dc_2008r2_en=[
        '#!ipxe\n',
        'set boot-url __boot_url__\n',
        'kernel /boot/pxe/wimboot\n',
        'initrd /boot/conf.d/s__srv_name__/install.bat install.bat\n',
        'initrd /boot/pxe/winpeshl.ini winpeshl.ini\n',
        'initrd /images/windows/2008r2_en/amd64/boot/bcd BCD\n',
        'initrd /images/windows/2008r2_en/amd64/boot/boot.sdi boot.sdi\n',
        'initrd /images/windows/2008r2_en/amd64/sources/boot.wim boot.wim\n',
        'initrd http://install.adman.cloud/api/v1.0/install/prestart/__srv_name__?token=__token__ api\n',
        'boot\n'
    ],
    windows_std_2008r2_ru=[
        '#!ipxe\n',
        'set boot-url __boot_url__\n',
        'kernel /boot/pxe/wimboot\n',
        'initrd /boot/conf.d/s__srv_name__/install.bat install.bat\n',
        'initrd /boot/pxe/winpeshl.ini winpeshl.ini\n',
        'initrd /images/windows/2008r2_ru/amd64/boot/bcd BCD\n',
        'initrd /images/windows/2008r2_ru/amd64/boot/boot.sdi boot.sdi\n',
        'initrd /images/windows/2008r2_ru/amd64/sources/boot.wim boot.wim\n',
        'initrd http://install.adman.cloud/api/v1.0/install/prestart/__srv_name__?token=__token__ api\n',
        'boot\n'
    ],
    windows_dc_2008r2_ru=[
        '#!ipxe\n',
        'set boot-url __boot_url__\n',
        'kernel /boot/pxe/wimboot\n',
        'initrd /boot/conf.d/s__srv_name__/install.bat install.bat\n',
        'initrd /boot/pxe/winpeshl.ini winpeshl.ini\n',
        'initrd /images/windows/2008r2_ru/amd64/boot/bcd BCD\n',
        'initrd /images/windows/2008r2_ru/amd64/boot/boot.sdi boot.sdi\n',
        'initrd /images/windows/2008r2_ru/amd64/sources/boot.wim boot.wim\n',
        'initrd http://install.adman.cloud/api/v1.0/install/prestart/__srv_name__?token=__token__ api\n',
        'boot\n'
    ],
    windows_std_2016_en=[
        '#!ipxe\n',
        'set boot-url __boot_url__\n',
        'kernel /boot/pxe/wimboot\n',
        'initrd /boot/conf.d/s__srv_name__/install.bat install.bat\n',
        'initrd /boot/pxe/winpeshl.ini winpeshl.ini\n',
        'initrd /images/windows/2016_en/amd64/boot/bcd BCD\n',
        'initrd /images/windows/2016_en/amd64/boot/boot.sdi boot.sdi\n',
        'initrd /images/windows/2016_en/amd64/sources/boot.wim boot.wim\n',
        'initrd http://install.adman.cloud/api/v1.0/install/prestart/__srv_name__?token=__token__ api\n',
        'boot\n'
    ],
    windows_std_2016_ru=[
        '#!ipxe\n',
        'set boot-url __boot_url__\n',
        'kernel /boot/pxe/wimboot\n',
        'initrd /boot/conf.d/s__srv_name__/install.bat install.bat\n',
        'initrd /boot/pxe/winpeshl.ini winpeshl.ini\n',
        'initrd /images/windows/2016_ru/amd64/boot/bcd BCD\n',
        'initrd /images/windows/2016_ru/amd64/boot/boot.sdi boot.sdi\n',
        'initrd /images/windows/2016_ru/amd64/sources/boot.wim boot.wim\n',
        'initrd http://install.adman.cloud/api/v1.0/install/prestart/__srv_name__?token=__token__ api\n',
        'boot\n'
    ],
    windows_std_2019_en=[
        '#!ipxe\n',
        'set boot-url __boot_url__\n',
        'kernel /boot/pxe/wimboot\n',
        'initrd /boot/conf.d/s__srv_name__/install.bat install.bat\n',
        'initrd /boot/pxe/winpeshl.ini winpeshl.ini\n',
        'initrd /images/windows/2019_en/amd64/boot/bcd BCD\n',
        'initrd /images/windows/2019_en/amd64/boot/boot.sdi boot.sdi\n',
        'initrd /images/windows/2019_en/amd64/sources/boot.wim boot.wim\n',
        'initrd http://install.adman.cloud/api/v1.0/install/prestart/__srv_name__?token=__token__ api\n',
        'boot\n'
    ],
    windows_std_2019_ru=[
        '#!ipxe\n',
        'set boot-url __boot_url__\n',
        'kernel /boot/pxe/wimboot\n',
        'initrd /boot/conf.d/s__srv_name__/install.bat install.bat\n',
        'initrd /boot/pxe/winpeshl.ini winpeshl.ini\n',
        'initrd /images/windows/2019_ru/amd64/boot/bcd BCD\n',
        'initrd /images/windows/2019_ru/amd64/boot/boot.sdi boot.sdi\n',
        'initrd /images/windows/2019_ru/amd64/sources/boot.wim boot.wim\n',
        'initrd http://install.adman.cloud/api/v1.0/install/prestart/__srv_name__?token=__token__ api\n',
        'boot\n'
    ]
)

os_list = [
    {'title': 'Ubuntu 14.04 LTS', 'os': 'ubuntu', 'osver': '14', "diskpart": ["0", "1"]},
    {'title': 'Ubuntu 16.04 LTS', 'os': 'ubuntu', 'osver': '16', "diskpart": ["0", "1"]},
    {'title': 'Ubuntu 18.04 LTS', 'os': 'ubuntu', 'osver': '18', "diskpart": ["0", "1"]},
    {'title': 'Ubuntu 20.04 LTS', 'os': 'ubuntu', 'osver': '20', "diskpart": ["0", "1"]},
    {'title': 'Debian 8', 'os': 'debian', 'osver': '8', "diskpart": ["0", "1"]},
    {'title': 'Debian 9', 'os': 'debian', 'osver': '9', "diskpart": ["0", "1"]},
    {'title': 'Debian 10', 'os': 'debian', 'osver': '10', "diskpart": ["0", "1"]},
    {'title': 'Centos 7', 'os': 'centos', 'osver': '7', "diskpart": ["0", "1"]},
    {'title': 'Centos 8', 'os': 'centos', 'osver': '8', "diskpart": ["0", "1"]},
    {'title': 'Windows Server 2012R2 Standard En', 'os': 'windows_std', 'osver': '2012r2_en', "diskpart": ["0"]},
    {'title': 'Windows Server 2012R2 Standard Ru', 'os': 'windows_std', 'osver': '2012r2_ru', "diskpart": ["0"]},
    {'title': 'Windows Server 2008R2 Standard En', 'os': 'windows_std', 'osver': '2008r2_en', "diskpart": ["0"]},
    {'title': 'Windows Server 2008R2 Standard Ru', 'os': 'windows_std', 'osver': '2008r2_ru', "diskpart": ["0"]},
    {'title': 'Windows Server 2016 Standard En', 'os': 'windows_std', 'osver': '2016_en', "diskpart": ["0"]},
    {'title': 'Windows Server 2016 Standard Ru', 'os': 'windows_std', 'osver': '2016_ru', "diskpart": ["0"]},
    {'title': 'Windows Server 2019 Standard En', 'os': 'windows_std', 'osver': '2019_en', "diskpart": ["0"]},
    {'title': 'Windows Server 2019 Standard Ru', 'os': 'windows_std', 'osver': '2019_ru', "diskpart": ["0"]},
    {'title': 'Windows Server 2008R2 Datacenter En', 'os': 'windows_dc', 'osver': '2008r2_en', "diskpart": ["0"]},
    {'title': 'Windows Server 2008R2 Datacenter Ru', 'os': 'windows_dc', 'osver': '2008r2_ru', "diskpart": ["0"]},
    {'title': 'Windows Server 2012R2 Datacenter En', 'os': 'windows_dc', 'osver': '2012r2_en', "diskpart": ["0"]},
    {'title': 'Windows Server 2012R2 Datacenter Ru', 'os': 'windows_dc', 'osver': '2012r2_ru', "diskpart": ["0"]}
]

