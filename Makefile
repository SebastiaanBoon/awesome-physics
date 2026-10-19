# Top-level entry point.
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Forwards every maintenance target to dev/Makefile so that `make all`,
# `make validate`, and the other commands work from the repository root.

TARGETS := help validate resources opml links all clean

.DEFAULT_GOAL := help
.PHONY: $(TARGETS)

$(TARGETS):
	@$(MAKE) --no-print-directory -C dev $@
