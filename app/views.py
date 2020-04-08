from app import app
import os
import shutil

# Function to Change root directory of the process.
def change_root_directory(path):
    try:
        os.chdir(path)
        os.chroot(path)
    except Exception as e:
        app.logger.debug('Не могу выполнить chroot: {}'.format(str(e)))
        pass

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/autoinst/api/v.1/complete/<server>')
def complete_install(server):


    default = dict(
        CHROOT_PATH='/opt/autoinst',
        GRUB_CONF_PATH='/srv/tftp/boot/grub/conf.d',
        TMP_GRUB_CONF_PATH='/var/grub',
        PRESEED_CONF_PATH='',
        SRV_NAME='s300'
    )

    real_root = os.open("/", os.O_RDONLY)

    # chroot
    change_root_directory(default['CHROOT_PATH'])

    app.logger.debug('chroot path')
    app.logger.debug(default['CHROOT_PATH'])

    tmp_grub_cfg = '{path}/{file}.cfg'.format(
        path=str(default['TMP_GRUB_CONF_PATH']),
        file=server
    )

    # print(tmp_grub_cfg)
    stream = os.popen('/usr/sbin/grub-mkconfig -o {}'.format(tmp_grub_cfg))
    output = stream.read()
    app.logger.debug(output)
    # os.system('/usr/sbin/grub-mkconfig -o {}'.format(tmp_grub_cfg))

    os.fchdir(real_root)
    os.chroot(".")

    # back to real root
    os.close(real_root)

    real_grub_cfg = '{chroot}{path}/{file}.cfg'.format(
        chroot=str(default['CHROOT_PATH']),
        path=str(default['TMP_GRUB_CONF_PATH']),
        file=server
    )

    # print(real_grub_cfg)

    if os.path.isfile(real_grub_cfg):
        # print ("File exist")

        grub_cfg = '{path}/{srv}/grub.cfg'.format(
            path=str(default['GRUB_CONF_PATH']),
            srv=server
        )
        os.remove(grub_cfg)
        shutil.copy(real_grub_cfg, grub_cfg)

    return '3'
