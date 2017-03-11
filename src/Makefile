#
# @SI_Copyright@
# Copyright (c) 2006 - 2014 StackIQ Inc. All rights reserved.
# 
# This product includes software developed by StackIQ Inc., these portions
# may not be modified, copied, or redistributed without the express written
# consent of StackIQ Inc.
# @SI_Copyright@
#

ifndef ROLL
include ../version.mk
endif

include order-$(ROLL).mk

order-$(ROLL).mk: Makefile ../version.mk $(shell find . -name version.mk)
	$(ROCKSBUILD)/bin/gen-order > $@


clean.order:
	-rm -f order-$(ROLL).mk

bootstrap rpm pkg clean nuke:
	@for dir in $(SRCDIRS); do			\
		(cd $$dir; $(MAKE) $@);			\
	done

dump-info::
	@for x in $(SRCDIRS); do			\
		if [ -d $$x ]; then			\
			(cd $$x; $(MAKE) $@); 		\
		fi;					\
	done
