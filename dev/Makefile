# Awesome Physics maintenance tasks.
# SPDX-License-Identifier: GPL-3.0-or-later

DEVDIR := $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST)))))
PYTHON ?= python3
SCRIPTS := $(DEVDIR)/scripts

.DEFAULT_GOAL := help
.PHONY: help hooks validate resources opml links site all clean

help: ## Show this help.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

hooks: ## Install the commit-msg hook and the commit template.
	git config core.hooksPath .githooks
	git config commit.template .gitmessage

validate: ## Check the structure and labels of every translation.
	$(PYTHON) $(SCRIPTS)/validate.py --readme $(DEVDIR)/../README.md
	$(PYTHON) $(SCRIPTS)/validate.py --readme $(DEVDIR)/../README.pt-BR.md

resources: ## Regenerate the catalogues from the READMEs.
	$(PYTHON) $(SCRIPTS)/parse_readme.py --lang en --input $(DEVDIR)/../README.md --output $(DEVDIR)/resources.json
	$(PYTHON) $(SCRIPTS)/parse_readme.py --lang pt-BR --input $(DEVDIR)/../README.pt-BR.md --output $(DEVDIR)/resources.pt-BR.json

opml: ## Regenerate dev/feeds.opml from dev/data/feeds.csv.
	$(PYTHON) $(SCRIPTS)/generate_opml.py

links: ## Check every URL in README.md (network required).
	$(PYTHON) $(SCRIPTS)/check_links.py --concurrency 16 --timeout 20

site: resources ## Build the static website into docs/.
	$(PYTHON) $(SCRIPTS)/build_site.py --lang en --source $(DEVDIR)/resources.json --output $(DEVDIR)/../docs/index.html
	$(PYTHON) $(SCRIPTS)/build_site.py --lang pt-BR --source $(DEVDIR)/resources.pt-BR.json --output $(DEVDIR)/../docs/pt-BR/index.html

all: resources opml validate ## Regenerate artifacts and validate.

clean: ## Remove generated artifacts.
	rm -f $(DEVDIR)/resources.json $(DEVDIR)/resources.pt-BR.json $(DEVDIR)/feeds.opml $(DEVDIR)/links-report.txt
	rm -rf $(DEVDIR)/../_site $(DEVDIR)/../docs/pt-BR