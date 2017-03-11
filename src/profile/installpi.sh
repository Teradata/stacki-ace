#!/bin/sh

#
# get the kickstart file
#
/opt/stack/bin/getprofile.py

#
# process the kickstart file
#
/opt/stack/bin/ksace.py

