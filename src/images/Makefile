# @SI_Copyright@
# @SI_Copyright@

ROLLROOT	= ../..
include $(STACKBUILD)/etc/CCRules.mk


build:
	mkdir -p boot
	(	cd boot ;				\
		tar xf ../boot-$(BOOTVER).tar.xz ;	\
		rm -rf overlays ;			\
		rm -f cmdline.txt config.txt kernel.img )
	

install::
	mkdir -p $(ROOT)/opt/stack/images/$(ARCH)
	$(INSTALL) -m444 boot/* $(ROOT)/opt/stack/images/$(ARCH)


refresh:
	wget https://downloads.raspberrypi.org/raspbian_lite/boot.tar.xz
	mv boot.tar.xz boot-$(shell date +%Y%m%d).tar.xz
	echo -e "NAME\t= stacki-ace-images" > version.mk
	echo -e "BOOTVER\t= $(shell date +%Y%m%d)" >> version.mk


clean::
	rm -rf boot
