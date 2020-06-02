#version=RHEL8
# System authorization information
# auth --enableshadow --passalgo=sha512
# Use graphical install
graphical
#text
# Run the Setup Agent on first boot
firstboot --enable
# Keyboard layouts
keyboard --vckeymap=us --xlayouts='us'
# System language
lang en_US.UTF-8

repo --name="AppStream" --baseurl=https://mirror.yandex.ru/centos/8/BaseOS/x86_64/os/../../../AppStream/x86_64/os/
# Use network installation
url --url="https://mirror.yandex.ru/centos/8/BaseOS/x86_64/os"
# Do not configure the X Window System
skipx
# System services
services --enabled="chronyd"
# System timezone
timezone Europe/Moscow --isUtc
# System bootloader configuration

%packages
@^minimal-environment
chrony
vim
%end

%addon com_redhat_kdump --disable --reserve-mb='auto'
%end

%anaconda
pwpolicy root --minlen=6 --minquality=1 --notstrict --nochanges --notempty
pwpolicy user --minlen=6 --minquality=1 --notstrict --nochanges --emptyok
pwpolicy luks --minlen=6 --minquality=1 --notstrict --nochanges --notempty
%end

%post --nochroot
sed -i 's/PermitRootLogin/#PermitRootLogin/' /mnt/sysimage/etc/ssh/sshd_config && echo 'PermitRootLogin yes' >> /mnt/sysimage/etc/ssh/sshd_config;
sed -i s/^SELINUX=.*$/SELINUX=disabled/ /mnt/sysimage/etc/selinux/config;
%end


