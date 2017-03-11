#!/opt/stack/bin/python

import shlex
import subprocess
import os
import shutil

##
## main
##
cmd = '/usr/bin/curl -o /run/ks.xml --local-port 1-66 --insecure https://10.1.31.1/install/sbin/profile.cgi?os=redhat&arch=armv7hl&np=4'
subprocess.call(shlex.split(cmd))

f = open('/run/ks.xml', 'r')
g = open('/run/ks.cfg', 'w')

cmd = '/opt/stack/bin/stack list host profile chapter=kickstart'
subprocess.call(shlex.split(cmd), stdin = f, stdout = g)

f.close()
g.close()

