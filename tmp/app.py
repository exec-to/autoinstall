# -*- coding: UTF-8 -*-
import os, sys 
import shutil

default = dict(
    CHROOT_PATH='/opt/autoinst',
    GRUB_CONF_PATH='/srv/tftp/boot/grub/conf.d',
    TMP_GRUB_CONF_PATH='/var/grub',
    PRESEED_CONF_PATH='',
    SRV_NAME='s300'
)

real_root = os.open("/", os.O_RDONLY)

# Function to Change root directory of the process. 
def change_root_directory(path): 
  
    try: 
        os.chdir(path) 
        os.chroot(path) 
    except Exception as exc: 
        error = DaemonOSEnvironmentError("Unable to change root directory ({exc})".format(exc = exc)) 
        raise error  
  
# chroot  
change_root_directory(default['CHROOT_PATH'])

tmp_grub_cfg = '{path}/{file}.cfg'.format(path=str(default['TMP_GRUB_CONF_PATH']), file=str(default['SRV_NAME']))
print(tmp_grub_cfg)

os.system('/usr/sbin/grub-mkconfig -o {}'.format(tmp_grub_cfg))

os.fchdir(real_root)
os.chroot(".")

# back to real root
os.close(real_root)

real_grub_cfg = '{chroot}{path}/{file}.cfg'.format(chroot=str(default['CHROOT_PATH']), path=str(default['TMP_GRUB_CONF_PATH']), file=str(default['SRV_NAME']))
print(real_grub_cfg)

if os.path.isfile(real_grub_cfg):
    print ("File exist")
    grub_cfg = '{path}/{srv}/grub.cfg'.format(path=str(default['GRUB_CONF_PATH']), srv=str(default['SRV_NAME']))
    os.remove(grub_cfg)
    shutil.copy(real_grub_cfg, grub_cfg)

