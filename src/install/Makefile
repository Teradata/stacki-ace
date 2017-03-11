# @SI_Copyright@
# @SI_Copyright@

ROLLROOT	= ../..
DEPENDS.FILES	= stacki-install.service
include $(STACKBUILD)/etc/CCRules.mk

build:

install::
	mkdir -p $(ROOT)/opt/stack/systemd
	$(INSTALL) -m644 stacki-install.service $(ROOT)/opt/stack/systemd

