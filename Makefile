# Top-level entry point.
# SPDX-License-Identifier: CC0-1.0
#
# Forwards every maintenance target to dev/Makefile so that `make all`,
# `make validate`, and the other commands work from the repository root.

TARGETS := help validate resources opml links all clean

.DEFAULT_GOAL := help
.PHONY: $(TARGETS)

$(TARGETS):
	@$(MAKE) --no-print-directory -C dev $@
