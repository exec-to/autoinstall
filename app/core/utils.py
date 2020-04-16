# -*- coding: UTF-8 -*-
from app import config
import os, sys, stat
import ipaddress
import hashlib


class Utils(object):

    @staticmethod
    def get_network_settings(ipaddr):
        addr4 = ipaddress.ip_address(ipaddr)
        gw = None
        nm = None
        found = False

        for subnet in config.local_networks:
            if addr4 in ipaddress.ip_network(subnet):
                gw = config.local_networks[subnet]['gateway']
                nm = config.local_networks[subnet]['netmask']
                found = True

        if not found:
            raise Exception("NotFound", "Не найдены настройки сети для указанного IP-адреса {}".format(str(addr4)))

        return [gw, nm]

    @staticmethod
    def get_token():
        return hashlib.md5(os.urandom(32)).hexdigest()

    @staticmethod
    def create_preseed_conf(adman_id, params, token):

        srv_dir = 's{srv}'.format(srv=adman_id)
        preseed_config = '{confdir}/{srv}/{srv}.seed'.format(
            confdir=config.grub['config-directory'],
            srv=srv_dir
        )

        preseed_template = '{preseeddir}/{os}{osver}.seed'.format(
            preseeddir=config.grub['preseed-directory'],
            os=params['os'].lower(),
            osver=params['osver'].lower()
        )

        mkconfig_cmd = '/bin/cp -f {src} {dst}'.format(
            src=preseed_template,
            dst=preseed_config
        )

        stream = os.popen(mkconfig_cmd)
        output = stream.read()

        # --

        gateway, netmask = Utils.get_network_settings(params['ipaddr'])

        # Read in the file
        with open(preseed_config, 'r') as file:
            filedata = file.read()

        # Replace the target string
        filedata = filedata.replace('__ipaddr__', str(params['ipaddr']))
        filedata = filedata.replace('__netmask__', netmask)
        filedata = filedata.replace('__gateway__', gateway)
        filedata = filedata.replace('__srv_name__', str(adman_id))
        filedata = filedata.replace('__passwdhash__', str(params['passwdhash']))
        filedata = filedata.replace('__token__', str(token))

        # Write the file out again
        with open(preseed_config, 'w') as file:
            file.write(filedata)

        os.chmod(preseed_config, 436)
