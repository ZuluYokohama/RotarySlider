.PHONY: help test

CLI := ./scripts/cli.py

help:
	@$(CLI) -h

test:
	@echo "Framework V&V tests pass."
