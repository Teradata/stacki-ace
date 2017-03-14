# @SI_Copyright@
# Copyright (c) 2006 - 2014 StackIQ Inc. All rights reserved.
# 
# This product includes software developed by StackIQ Inc., these portions
# may not be modified, copied, or redistributed without the express written
# consent of StackIQ Inc.
# @SI_Copyright@
#
#

PKROOT = /opt/stack
ROLLROOT = ../../
DEPENDS.DIR = stack
PYFILES = $(shell find stack/commands -type f -name \*.py)
INITPYFILES = $(shell find stack/commands -type f -name __init__.py)
DEPENDS.FILES=$(PYFILES)

include $(STACKBUILD)/etc/CCRules.mk


build:
	for i in $(INITPYFILES); do \
		echo $$i | awk '{ print "\nRollName = \"$(ROLL)\"" >> $$1;}';\
	done;

install::
	mkdir -p $(ROOT)/$(PY.STACK)/
	find stack -type f -name \*.py | cpio -pudv $(ROOT)/$(PY.STACK)/

clean::
	find stack -type f -name \*.pyc -exec rm -rf {} \;
