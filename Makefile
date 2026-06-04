.PHONY: help test

CLI := ./scripts/cli.py

help:
	@$(CLI) -h

test:
	@echo "Running Framework V&V Tests..."
	@python3 -m unittest discover -s tests -p "test_*.py"
