# -*- coding: UTF-8 -*-
from app import config


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
        return output
        # api.logger.debug({"mkconfig_cmd": output})

    @staticmethod
    def update_template(args):
        setup_cmd = '{prog} {template}'.format(
            prog=config.grub['setup_script'],
            template=config.grub['templates'][args.os][args.osver]
        )

        stream = os.popen(setup_cmd)
        output = stream.read()
        return output
        # api.logger.debug(output)
        # api.logger.debug({"setup_cmd": output})




