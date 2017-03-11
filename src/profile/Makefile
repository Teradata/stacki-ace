# @SI_Copyright@
# @SI_Copyright@

ROLLROOT	= ../..
DEPENDS.FILES	= getprofile.py ksace.py installpi.sh

include $(STACKBUILD)/etc/CCRules.mk


build:

install::
	mkdir -p $(ROOT)/opt/stack/bin
	$(INSTALL) -m755 getprofile.py $(ROOT)/opt/stack/bin/
	$(INSTALL) -m755 ksace.py $(ROOT)/opt/stack/bin/
	$(INSTALL) -m755 installpi.sh $(ROOT)/opt/stack/bin/

