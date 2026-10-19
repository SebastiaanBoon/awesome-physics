# Awesome Physics maintenance tasks.
# SPDX-License-Identifier: GPL-3.0-or-later

DEVDIR := $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST)))))
PYTHON ?= python3
SCRIPTS := $(DEVDIR)/scripts

.DEFAULT_GOAL := help
.PHONY: help validate resources opml links site all clean

help: ## Show this help.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

validate: ## Check the structure and labels of README.md.
	$(PYTHON) $(SCRIPTS)/validate.py

resources: ## Regenerate dev/resources.json from README.md.
	$(PYTHON) $(SCRIPTS)/parse_readme.py

opml: ## Regenerate dev/feeds.opml from dev/data/feeds.csv.
	$(PYTHON) $(SCRIPTS)/generate_opml.py

links: ## Check every URL in README.md (network required).
	$(PYTHON) $(SCRIPTS)/check_links.py --concurrency 16 --timeout 20

site: resources ## Build the static website into docs/index.html.
	$(PYTHON) $(SCRIPTS)/build_site.py --output $(DEVDIR)/../docs/index.html

all: resources opml validate ## Regenerate artifacts and validate.

clean: ## Remove generated artifacts.
	rm -f $(DEVDIR)/resources.json $(DEVDIR)/feeds.opml $(DEVDIR)/links-report.txt
	rm -rf $(DEVDIR)/../_site