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
        # TODO: Copy windows preseed to share dir (Mount conf share /boot/conf.d/srv_name/)
        preseed_template = '{preseeddir}/{os}{osver}_{diskpart}.seed'.format(
            preseeddir=config.utils['preseed-directory'],
            os=params['os'].lower(),
            osver=params['osver'].lower(),
            diskpart=params['diskpart'].lower()
        )

        preseed_config = '{confdir}/s{srv}/s{srv}.seed'.format(
            confdir=config.utils['config-directory'],
            srv=adman_id
        )

        mkconfig_cmd = '/bin/cp -f {src} {dst}'.format(
            src=preseed_template,
            dst=preseed_config
        )

        stream = os.popen(mkconfig_cmd)
        output = stream.read()

        # -- Fill template

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

    @staticmethod
    def create_server_dir(server_id):
        create_cmd = "/bin/mkdir {dir}/s{server_id}".format(
            dir=config.utils['config-directory'],
            server_id=server_id
        )

        stream = os.popen(create_cmd)
        output = stream.read()
        return output

    @staticmethod
    def remove_symbol_link(link):
        rm_cmd = "/bin/rm -f {dir}/{link}".format(
            dir = config.utils['config-directory'],
            link=link
        )

        stream = os.popen(rm_cmd)
        output = stream.read()
        return output

    @staticmethod
    def create_symbol_link(server_id, link):
        os.chdir(config.utils['config-directory'])
        create_cmd = "/bin/ln -s s{server_id} {link}".format(
            server_id=server_id,
            link=link
        )

        stream = os.popen(create_cmd)
        output = stream.read()
        return output

    @staticmethod
    def create_config(args, adman_id, token=''):
        ipxe_config = '{confdir}/s{srv}/boot.ipxe'.format(
            confdir=config.utils['config-directory'],
            srv=adman_id
        )

        tpl_key = "{os}_{osver}".format(os = args['os'].lower(), osver = args['osver'].lower())
        tpl = config.templates[tpl_key]

        with open(ipxe_config, 'a') as file:
            file.truncate(0)
            file.writelines(tpl)

        # Read in the file
        with open(ipxe_config, 'r') as file:
            filedata = file.read()

        # Replace the target string
        filedata = filedata.replace('__srv_name__', str(adman_id))
        filedata = filedata.replace('__boot_url__', str(config.utils['boot_url']))
        filedata = filedata.replace('__token__', str(token))

        # Write the file out again
        with open(ipxe_config, 'w') as file:
            file.write(filedata)

        os.chmod(ipxe_config, 436)

    @staticmethod
    def create_install_bat(args, adman_id):
        bat_config = '{confdir}/s{srv}/install.bat'.format(
            confdir=config.utils['config-directory'],
            srv=adman_id
        )

        osver = args['osver'].lower()

        with open(bat_config, 'a') as file:
            file.truncate(0)
            file.write('wpeinit\n')
            # TODO: fix backslash in path
            file.write('net use j: \\\\__boot_host__\\images\\__os_ver__\\amd64\n')
            file.write('net use k: \\\\__boot_host__\\configfile\n')
            file.write('j:\\setup.exe /unattend:k:\\s__srv_name__\\s__srv_name__.seed\n')

        # Read in the file
        with open(bat_config, 'r') as file:
            filedata = file.read()

        # Replace the target string
        filedata = filedata.replace('__srv_name__', str(adman_id))
        filedata = filedata.replace('__os_ver__', str(osver))
        filedata = filedata.replace('__boot_host__', str(config.utils['boot_host']))

        # Write the file out again
        with open(bat_config, 'w') as file:
            file.write(filedata)

        os.chmod(bat_config, 436)

    @staticmethod
    def remove_install_bat(adman_id):
        bat_config = '{confdir}/s{srv}/install.bat'.format(
            confdir=config.utils['config-directory'],
            srv=adman_id
        )

        if os.path.exists(bat_config):
            os.remove(bat_config)

    @staticmethod
    def remove_preseed_conf(adman_id):
        preseed_config = '{confdir}/s{srv}/s{srv}.seed'.format(
            confdir=config.utils['config-directory'],
            srv=adman_id
        )

        if os.path.exists(preseed_config):
            os.remove(preseed_config)