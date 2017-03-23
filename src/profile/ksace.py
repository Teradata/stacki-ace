#!/usr/bin/python

from pykickstart.parser import *
from pykickstart.sections import *
from pykickstart.version import makeVersion

import shlex
import subprocess
import os
import shutil
import sys

if not os.path.exists('/run/ks.cfg'):
	sys.exit(0)

ksparser = KickstartParser(makeVersion())
ksparser.readKickstart("/run/ks.cfg")


def findBootDisk():
	p = subprocess.Popen([ '/usr/bin/lsblk', '-nlo', 'NAME,MOUNTPOINT' ],
		stdin=subprocess.PIPE, stdout=subprocess.PIPE,
		stderr=subprocess.PIPE)
	o = p.communicate()[0]

	for line in o.split('\n'):
		l = line.split()
		if len(l) == 2 and l[1] == '/boot':
			return l[0]

	p = subprocess.Popen([ '/usr/bin/cat', '/proc/mounts' ],
		stdin=subprocess.PIPE, stdout=subprocess.PIPE,
		stderr=subprocess.PIPE)
	o = p.communicate()[0]

	for line in o.split('\n'):
		l = line.split()
		if len(l) > 2 and l[1] == '/' and l[2] == 'nfs':
			return 'nfs'

	return None


def doScript(section, script, scriptnum):
	fname = '/run/ks-script-%s-%d' % (section, scriptnum)

	f = open(fname, 'w')
	f.write('#!%s\n\n' % script.interp)
	
	s = '%s' % script
	for line in s.split('\n'):
		if line.startswith('%pre') or line.startswith('%post') \
				or line.startswith('%end'):
			#
			# skip
			#
			continue

		f.write('%s\n' % line)

	f.close()
	os.chmod(fname, 0700)

	pid = os.fork()

	if pid == 0:
		if section == 'post' and script.inChroot:
			shutil.copy(fname, '/run/mnt/sysimage%s' % fname)
			os.chroot('/run/mnt/sysimage')

		#
		# set stdout and stderr to files on the disk so we can examine
		# the output and errors
		#
		fout = open('%s.out' % fname, 'w')
		ferr = open('%s.err' % fname, 'w')
		
		subprocess.call([ fname ], stdout = fout, stderr = ferr)

		fout.close()
		ferr.close()
		sys.exit(0)
	else:
		os.wait()

##
## MAIN
##

#
# first determine if we should execute this script
#
sys.path.append('/run')

try:
	import ace_config

	action = ace_config.attributes['bootaction']
	appliance = ace_config.attributes['appliance']
except:
	action = None
	appliance = None

if 0:
	if not appliance:
		#
		# do nothing because this is not an ACE backend node
		#
		sys.exit(0)

if action != 'install':
	print 'ksace.py: bootaction "%s" != "install"' % action
	print 'ksace.py: exiting'
	sys.exit(0)

#
# action == 'install'
#
# determine if we booted off the network -- which means our /boot partition
# will be an nfs mount.
#

bootdisk = findBootDisk()

if bootdisk != 'nfs':
	#
	# we didn't boot off the network, then remove /boot/bootcode.bin
	# and reboot.
	#
	# we want the node to go through the possible boot devices and
	# eventually boot off the ethernet network port. this progression is
	# described here:
	#
	# https://www.raspberrypi.org/documentation/hardware/raspberrypi/bootmodes/bootflow.md
	#

	os.remove('/boot/bootcode.bin')
	
else:
	#
	# we booted off the network and action == 'install', so let's install
	# the node
	#

	#
	# do the pre sections
	#
	scriptnum = 0

	for script in ksparser.handler.scripts:
		if script.type == KS_SCRIPT_PRE:
			doScript('pre', script, scriptnum)
			scriptnum += 1

	#
	# install the packages
	#
	packages = []
	p = '%s' % ksparser.handler.packages
	for line in p.split('\n'):
		if line.startswith('%package') or line.startswith('%end') \
				or len(line) == 0:
			#
			# skip
			#
			continue

		packages.append('%s' % line)

	myenv = os.environ.copy()
	myenv['TMPDIR'] = '/run/mnt/sysimage/var/tmp'

	cmd = '/usr/bin/yum --installroot=/run/mnt/sysimage --config=/run/mnt/sysimage/etc/yum.repos.d/stacki.repo install -y %s' % ' '.join(packages)

	subprocess.call(shlex.split(cmd), env = myenv)

	#
	# do the post sections
	#
	if not os.path.exists('/run/mnt/sysimage/run'):
		os.makedirs('/run/mnt/sysimage/run')

	for script in ksparser.handler.scripts:
		if script.type == KS_SCRIPT_POST:
			doScript('post', script, scriptnum)
			scriptnum += 1

	#
	# save the installation messages
	#
	shutil.copy('/run/ksace.debug', '/run/mnt/sysimage/root/ksace.debug')

#
# reboot
#
cmd = '/usr/sbin/reboot'
subprocess.call(shlex.split(cmd))

