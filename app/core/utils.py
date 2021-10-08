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
                pr = config.local_networks[subnet]['prefix']
                found = True

        if not found:
            raise Exception("NotFound", "Не найдены настройки сети для указанного IP-адреса {}".format(str(addr4)))

        return [gw, nm, pr]


    @staticmethod
    def get_dhcp_addr(ipaddr):
        addr4 = ipaddress.ip_address(ipaddr) + 1
        return str(addr4)


    @staticmethod
    def get_token():
        return hashlib.md5(os.urandom(32)).hexdigest()

    @staticmethod
    def create_preseed_conf(adman_id, params, token):
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

        gateway, netmask, _ = Utils.get_network_settings(params['ipaddr'])

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
        filedata = filedata.replace('__boot_host__', str(config.utils['boot_host']))

        # Write the file out again
        with open(preseed_config, 'w') as file:
            file.write(filedata)

        os.chmod(preseed_config, 436)

    @staticmethod
    def create_server_dir(server_id):
        create_cmd = "/bin/mkdir -p {dir}/s{server_id}".format(
            dir=config.utils['config-directory'],
            server_id=server_id
        )

        stream = os.popen(create_cmd)
        output = stream.read()
        return output

    @staticmethod
    def remove_symbol_link(link):
        rm_cmd = "/bin/rm -rf {dir}/{link}".format(
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

        diskpart = int(args['diskpart'])
        conf_dir = str(config.utils['config-directory'])
        url = ""

        if diskpart == 2:
            url = str(config.utils['iscsi_url'])
        else:
            url = str(config.utils['boot_url'])

        ipxe_config = '{confdir}/s{srv}/boot.ipxe'.format(
            confdir=conf_dir,
            srv=adman_id
        )

        tpl_key = "{os}_{osver}".format(os = args['os'].lower(), osver = args['osver'].lower())
        if diskpart == 2 and args['os'].lower() == 'local':
            tpl_key = "{os}_{osver}".format(os=args['os'].lower(), osver=2)

        tpl = config.templates[tpl_key]

        with open(ipxe_config, 'a') as file:
            file.truncate(0)
            file.writelines(tpl)

        # Read in the file
        with open(ipxe_config, 'r') as file:
            filedata = file.read()

        # Replace the target string
        filedata = filedata.replace('__srv_name__', str(adman_id))
        filedata = filedata.replace('__boot_url__', url)
        filedata = filedata.replace('__token__', str(token))

        # Write the file out again
        with open(ipxe_config, 'w') as file:
            file.write(filedata)

        os.chmod(ipxe_config, 436)

    @staticmethod
    def create_dhcp_config(adman_id, mac_addr, dhcp_addr, router=True):

        conf_dir = "/srv/hosts"
        dhcp_config = '{confdir}/s{srv}.conf'.format(
            confdir=conf_dir,
            srv=adman_id
        )

        with open(dhcp_config, 'a') as file:
            file.truncate(0)
            port_number = 0
            tpl_list = []
            for mac in mac_addr:
                tpl_list.append('#Autogenerated DHCP configuration\n')
                tpl_list.append('  host s{srv_name}p{port_number} {{\n'.format(srv_name=adman_id, port_number=port_number))
                tpl_list.append('    hardware ethernet {mac_addr};\n'.format(mac_addr=mac.mac_addr))
                tpl_list.append('    fixed-address {dhcp_addr};\n'.format(dhcp_addr=dhcp_addr))
                if router:
                    tpl_list.append('    option routers 10.0.224.4;\n')
                tpl_list.append('  }\n\n')
                port_number += 1

            file.writelines(tpl_list)

        os.chmod(dhcp_config, 436)


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
            file.write('ping 10.0.222.1\n')
            file.write('ping 10.0.222.1\n')
            file.write('ping 10.0.222.1\n')
            file.write('net use j: \\\\__boot_host__\\images\\__os_ver__\\amd64 /user:user pass\n')
            file.write('net use k: \\\\__boot_host__\\configfile /user:user pass\n')
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
    def create_win_set_ip_ps(ipaddr, token, adman_id):
        ps_config = '{confdir}/s{srv}/set-ip.ps1'.format(
            confdir=config.utils['config-directory'],
            srv=adman_id
        )

        with open(ps_config, 'a') as file:
            file.truncate(0)
            file.write('$ifaceindex = get-wmiobject win32_networkadapter -filter "netconnectionstatus = 2" | select -expand InterfaceIndex; ')
            file.write('netsh interface ipv4 set address name=$ifaceindex source=static addr=__ip_addr__  mask=__netmask__ gateway=__gateway__ gwmetric=1; ')
            file.write('netsh interface ipv4 add dns $ifaceindex 8.8.8.8 index=1; ')
            file.write('Timeout /T 15; ')
            file.write('ping 8.8.8.8; ')
            file.write('[System.Net.WebRequest]::Create("http://install.adman.cloud/api/v1.0/install/complete/__srv_name__?token=__token__").GetResponse(); ')

        gateway, netmask, _ = Utils.get_network_settings(ipaddr)
        # Read in the file
        with open(ps_config, 'r') as file:
            filedata = file.read()

        # Replace the target string
        filedata = filedata.replace('__ip_addr__', str(ipaddr))
        filedata = filedata.replace('__netmask__', netmask)
        filedata = filedata.replace('__gateway__', gateway)
        filedata = filedata.replace('__srv_name__', str(adman_id))
        filedata = filedata.replace('__token__', token)

        # Write the file out again
        with open(ps_config, 'w') as file:
            file.write(filedata)

        os.chmod(ps_config, 436)


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


    @staticmethod
    def remove_win_set_ip_ps(adman_id):
        ps_config = '{confdir}/s{srv}/set-ip.ps1'.format(
            confdir=config.utils['config-directory'],
            srv=adman_id
        )

        if os.path.exists(ps_config):
            os.remove(ps_config)
