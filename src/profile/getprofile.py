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

cmdline.close()

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

f.close()
g.close()

