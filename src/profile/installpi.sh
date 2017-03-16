#!/bin/sh

#
# get the kickstart file
#
(cd /run ; /opt/stack/bin/getprofile.py 2>&1 | tee /run/getprofile.debug)

#
# process the kickstart file
#
(cd /run ; /opt/stack/bin/ksace.py 2>&1 | tee /run/ksace.debug /dev/tty1)

