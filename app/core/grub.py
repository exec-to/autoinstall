# -*- coding: UTF-8 -*-
from app import config
import os, sys, stat


class Grub(object):

    @staticmethod
    def mkconfig(adman_id):
        srv_dir = 's{srv}'.format(srv=adman_id)
        grub_config = '{confdir}/{srv}/grub.cfg'.format(
            confdir=config.grub['config-directory'],
            srv=srv_dir
        )

        mkconfig_cmd = '{prog} -o {dst}'.format(
            prog=config.grub['mkconfig-script'],
            dst=grub_config
        )

        stream = os.popen(mkconfig_cmd)
        output = stream.read()

        # Read in the file
        with open(grub_config, 'r') as file:
            filedata = file.read()

        # Replace the target string
        filedata = filedata.replace('__srv_name__', str(adman_id))

        # Write the file out again
        with open(grub_config, 'w') as file:
            file.write(filedata)

        os.chmod(grub_config, 436)

        return output
        # api.logger.debug({"mkconfig_cmd": output})

    @staticmethod
    def update_template(args):
        setup_cmd = '{prog} {template}'.format(
            prog=config.grub['setup_script'],
            template=config.grub['templates'][args['os']][args['osver']]
        )

        stream = os.popen(setup_cmd)
        output = stream.read()
        return output
        # api.logger.debug(output)
        # api.logger.debug({"setup_cmd": output})


    @staticmethod
    def create_symbol_link(server_id, link):
        os.chdir(config.grub['config-directory'])
        create_cmd = "/bin/ln -s s{server_id} {link}".format(
            server_id=server_id,
            link=link
        )

        stream = os.popen(create_cmd)
        output = stream.read()
        return output

    @staticmethod
    def remove_symbol_link(link):
        rm_cmd = "/bin/rm -f {dir}/{link}".format(
            dir = config.grub['config-directory'],
            link=link
        )

        stream = os.popen(rm_cmd)
        output = stream.read()
        return output

    @staticmethod
    def create_server_dir(server_id):
        create_cmd = "/bin/mkdir {dir}/s{server_id}".format(
            dir=config.grub['config-directory'],
            server_id=server_id
        )

        stream = os.popen(create_cmd)
        output = stream.read()
        return output

