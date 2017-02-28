#!/opt/stack/bin/python

import shlex
import subprocess
import os
import shutil


def nukedisk(disk):
	#
	# nuke disk
	#
	cmd = '/usr/bin/dd if=/dev/zero of=/dev/%s bs=512 count=1024' % disk
	print 'cmd: %s' % cmd
	subprocess.call(shlex.split(cmd))

	cmd = '/usr/sbin/parted -s /dev/%s mklabel msdos' % disk
	print 'cmd: %s' % cmd
	subprocess.call(shlex.split(cmd))


def partition(disk):
	#
	# partition
	#
	cmd = '/usr/sbin/parted -s /dev/%s ' % disk
	cmd += 'mkpart primary fat32 0% 100M'
	print 'cmd: %s' % cmd
	subprocess.call(shlex.split(cmd))

	cmd = '/usr/sbin/parted -s /dev/%s ' % disk
	cmd += 'mkpart primary ext4 100M 100%'
	print 'cmd: %s' % cmd
	subprocess.call(shlex.split(cmd))


def diskformat(bootpart, rootpart):
	#
	# format
	#
	cmd = '/usr/sbin/mkfs -t vfat /dev/%s' % bootpart
	print 'cmd: %s' % cmd
	subprocess.call(shlex.split(cmd))

	cmd = '/usr/sbin/mkfs -t ext4 /dev/%s' % rootpart
	print 'cmd: %s' % cmd
	subprocess.call(shlex.split(cmd))


def mount(bootpart, rootpart):
	#
	# mount
	#
	if not os.path.exists('/run/mnt/sysimage'):
		os.makedirs('/run/mnt/sysimage')

	cmd = '/usr/bin/mount /dev/%s /run/mnt/sysimage' % rootpart
	print 'cmd: %s' % cmd
	subprocess.call(shlex.split(cmd))

	cwd = os.getcwd()
	os.chdir('/run/mnt/sysimage')
	if not os.path.exists('./boot'):
		os.mkdir('boot')

	cmd = '/usr/bin/mount /dev/%s boot' % bootpart
	print 'cmd: %s' % cmd
	subprocess.call(shlex.split(cmd))

	os.chdir(cwd)
	

def packageinstall():
	#
	# package install
	#
	if not os.path.exists('/run/mnt/sysimage/etc/yum.repos.d'):
		os.makedirs('/run/mnt/sysimage/etc/yum.repos.d')

	f = open('/run/mnt/sysimage/etc/yum.repos.d/stacki.repo', 'w')
	f.write("""[stacki-4.0_20170208-7.x]
name=stacki 4.0_20170208 7.x
baseurl=http://10.1.31.1/install/pallets/stacki/4.0_20170208/7.x/redhat/armv7hl
assumeyes=1
gpgcheck=0
[CentOS-7-7.x]
name=CentOS 7 7.x
baseurl=http://10.1.31.1/install/pallets/CentOS/7/7.x/redhat/armv7hl
assumeyes=1
gpgcheck=0
[CentOS-kernel-rpi2-7-7.x]
name=CentOS-kernel-rpi2 7 7.x
baseurl=http://10.1.31.1/install/pallets/CentOS-kernel-rpi2/7/7.x/redhat/armv7hl
assumeyes=1
gpgcheck=0""")
	f.close()

	myenv = os.environ.copy()
	myenv['TMPDIR'] = 'TMPDIR=/run/mnt/sysimage/var/tmp'

	packages = [ '@core', 'raspberrypi2-kernel', 'raspberrypi2-firmware',
		'raspberrypi2-kernel-firmware', 'foundation-python' ]

	cmd = '/usr/bin/yum --installroot=/run/mnt/sysimage --config=/run/mnt/sysimage/etc/yum.repos.d/stacki.repo install -y %s' % ' '.join(packages)
	print 'cmd: %s' % cmd
	subprocess.call(shlex.split(cmd), env = myenv)

	cmd = 'rm -f /run/mnt/sysimage/etc/yum.repos.d/CentOS*.repo'
	print 'cmd: %s' % cmd
	subprocess.call(shlex.split(cmd))
	

def postscripts():
	#
	# root password
	#
	f = open('/run/mnt/sysimage/etc/shadow', 'r')
	newshadow = open('/run/mnt/sysimage/etc/shadow.new', 'w')

	for line in f.readlines():
		l = line.split(':')
		if l[0] == 'root':
			l[1] = '$6$YmwsFK8f$9JULr6BDbaKk9lDUkC3qgO56aZqvUUYAnafavppHAUy2wWWFzaTaFPB/e1VuZf/xzBt9oaCMbRmd0OyYxdmkd1'

		newshadow.write('%s' % ':'.join(l))

	f.close()
	newshadow.close()

	shutil.move('/run/mnt/sysimage/etc/shadow.new',
		'/run/mnt/sysimage/etc/shadow')

	#
	# boot files
	#
	f = open('/run/mnt/sysimage/boot/cmdline.txt', 'w')
	f.write('dwc_otg.lpm_enable=0 root=/dev/%s rootfstype=ext4 elevator=deadline rootwait\n' % rootpart)
	f.close()

	f = open('/run/mnt/sysimage/boot/config.txt', 'w')
	f.write('program_usb_boot_mode=1\n')
	f.close()

	#
	# /etc/fstab
	#
	f = open('/run/mnt/sysimage/etc/fstab', 'w')
	f.write('/dev/%s /boot vfat noatime 0 0\n' % bootpart)
	f.write('/dev/%s / ext4 noatime 0 0\n' % rootpart)
	f.close()

	#
	# networking
	#
	f = open('/run/mnt/sysimage/etc/sysconfig/network', 'w')
	f.write('NETWORKING=yes\n')
	f.write('HOSTNAME=rasp002.stacki.com\n')
	f.close()

	f = open('/run/mnt/sysimage/etc/sysconfig/network-scripts/ifcfg-eth0',
		'w')
	f.write('DEVICE=eth0\n')
	f.write('HWADDR=b8:27:eb:ad:75:bd\n')
	f.write('IPADDR=10.1.31.2\n')
	f.write('NETMASK=255.255.0.0\n')
	f.write('BOOTPROTO=static\n')
	f.write('ONBOOT=yes\n')
	f.write('MTU=1500\n')
	f.close()

	#
	# hostname
	#
	f = open('/run/mnt/sysimage/etc/hostname', 'w')
	f.write('rasp002.stacki.com\n')
	f.close()

	#
	# disable selinux
	#
	f = open('/run/mnt/sysimage/etc/selinux/config', 'w')
	f.write('SELINUX=disabled\n')
	f.close()

	#
	# authorized_keys
	#
	if not os.path.exists('/run/mnt/sysimage/root/.ssh'):
		os.makedirs('/run/mnt/sysimage/root/.ssh')

	f = open('/run/mnt/sysimage/root/.ssh/authorized_keys', 'w')

	f.write("""ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCyt/3AUmNZn8vx7tM1fmONthe37MlRWB2/Ku1dveh3vnluBKriKnbqVE9tNeGs+h4oTr22Egk2vjctC9qT1HQ1DwQGn9LJPE5uIGvMQPs1s8vVSaUVL4uTyLDAvApERpxGPNYp1VPTDxmppqB215yaGcfKYCcOye6eEOHcZt4GJyllF1jvQtDbhJMFb0VO/6EaBCraO3+pI1kFUgie8hMDqFoM047jL9G8Sl8zSZ95of3wssT4sJFJ6f5oeA9H4S77t68DqStl3/nic2296F4UutD7mPiZNBl1ccgxFM/eANsOMVL2raurmdcl1qrauPr0pc+hzvuSAiAaV0NKYXRD root@rasp001.stacki.com\n""")

	f.close()


def reboot():
	#
	# reboot
	#
	cmd = '/usr/bin/umount /run/mnt/sysimage/boot'
	print 'cmd: %s' % cmd
	subprocess.call(shlex.split(cmd))

	cmd = '/usr/bin/umount /run/mnt/sysimage'
	print 'cmd: %s' % cmd
	subprocess.call(shlex.split(cmd))

	cmd = '/usr/sbin/reboot'
	print 'cmd: %s' % cmd
	subprocess.call(shlex.split(cmd))

##
## main
##

# bootdisk = 'sda'
bootdisk = 'mmcblk0'

if bootdisk == 'sda':
	bootpart = 'sda1'
	rootpart = 'sda2'
elif bootdisk == 'mmcblk0':
	bootpart = 'mmcblk0p1'
	rootpart = 'mmcblk0p2'

nukedisk(bootdisk)
partition(bootdisk)
diskformat(bootpart, rootpart)
mount(bootpart, rootpart)
packageinstall()
postscripts()
reboot()

