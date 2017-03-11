# @SI_Copyright@
# @SI_Copyright@

ROLLROOT	= ../..
# DEPENDS.DIRS	= etc init.d
include $(STACKBUILD)/etc/CCRules.mk

build:

install::
	mkdir -p $(ROOT)/opt/stack/images
	$(INSTALL) -m444 kernel7.img $(ROOT)/opt/stack/images

