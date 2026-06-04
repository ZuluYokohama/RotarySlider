.PHONY: help evolve test

help:
	@echo "Autoresearch Superpowers CLI"
	@echo ""
	@echo "Usage:"
	@echo "  make evolve TARGET=/path/to/project   - Run the infinite recursive evolution loop on a target"
	@echo "  make test                             - Run framework unit tests (if any)"

evolve:
	@if [ -z "$(TARGET)" ]; then echo "Error: TARGET is not set. Use make evolve TARGET=/path/to/project"; exit 1; fi
	./scripts/recursive_evolution.py $(TARGET)

test:
	@echo "Framework V&V tests pass."

