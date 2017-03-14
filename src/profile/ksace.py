#!/usr/bin/python

from pykickstart.parser import *
from pykickstart.sections import *
from pykickstart.version import makeVersion

import shlex
import subprocess
import os
import shutil
import sys

ksparser = KickstartParser(makeVersion())
ksparser.readKickstart("/run/ks.cfg")

# print dir(ksparser.handler)
# print dir(ksparser.handler.scripts)

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
# reboot
#
cmd = '/usr/sbin/reboot'
# subprocess.call(shlex.split(cmd))

