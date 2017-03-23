#!/opt/stack/bin/python

import shlex
import subprocess
import os
import shutil

##
## main
##

#
# parse out the IP address of the frontend
#
cmdline = open('/proc/cmdline', 'r')

frontend = None
for cmdarg in cmdline.readline().split():
	if cmdarg.startswith('frontend='):
		frontend = cmdarg.split('=')[1]
		break

cmdline.close()

if not frontend:
	#
	# this is the first time this node is being configured, that is, it
	# is a backend node and it booted with the default stacki-centos.img.
	# DHCP is enabled, so let's go get the frontend IPs address from the
	# NetworkManager (dhclient) configuration.
	#

	import glob

	path = '/var/lib/NetworkManager/dhclient*lease'

	for filename in glob.glob(path):
		f = open(filename, 'r')
		for line in f.readlines():
			l = line.split()
			if len(l) > 2 and l[1] == 'dhcp-server-identifier':
				frontend = l[2].strip(';')

if not frontend:
	#
	# can't find the frontend, so print an message and exit
	#
	print 'Cannot find a frontend'
	sys.exit(0)

#
# count the number of CPUs
#
np = 0

cpuinfo = open('/proc/cpuinfo', 'r')

for line in cpuinfo.readlines():
	l = line.split(':')
	if len(l) > 0 and l[0].strip() == 'processor':
		np += 1

cpuinfo.close()

if np ==0:
	np = 1

cmd = '/usr/bin/curl -o /run/ks.xml --local-port 1-66 --insecure https://%s/install/sbin/profile.cgi?os=redhat&arch=armv7hl&np=%d' % (frontend, np)
subprocess.call(shlex.split(cmd))

f = open('/run/ks.xml', 'r')
g = open('/run/ks.cfg', 'w')

cmd = '/opt/stack/bin/stack list host profile chapter=kickstart'
subprocess.call(shlex.split(cmd), stdin = f, stdout = g)

#
# need to seek back to the beginning of /run/ks.xml for the next command
#
f.seek(0)

h = open('/run/ace_config.py', 'w')
cmd = '/opt/stack/bin/stack list host profile chapter=stacki'
subprocess.call(shlex.split(cmd), stdin = f, stdout = h)

f.close()
g.close()
h.close()

