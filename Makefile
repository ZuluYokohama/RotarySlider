.PHONY: help test oracle evolve

CLI := ./scripts/cli.py
ORACLE := ./scripts/oracle.py

help:
	@$(CLI) -h
	@echo "\nAdvanced Commands:"
	@echo "  make oracle TARGET=/path    - Run the AST static analyzer to auto-inject intent vectors"

test:
	@echo "Running Framework V&V Tests..."
	@python3 -m unittest discover -s tests -p "test_*.py"

oracle:
	@if [ -z "$(TARGET)" ]; then echo "Error: TARGET is not set. Use make oracle TARGET=/path"; exit 1; fi
	$(ORACLE) $(TARGET)

evolve:
	@if [ -z "$(TARGET)" ]; then echo "Error: TARGET is not set. Use make evolve TARGET=/path"; exit 1; fi
	$(CLI) evolve $(TARGET)

yolo:
	@if [ -z "$(TARGET)" ]; then echo "Error: TARGET is not set. Use make yolo TARGET=/path"; exit 1; fi
	./scripts/chaos_monkey.py $(TARGET)
	@echo "Chaos injected. Run 'make evolve TARGET=$(TARGET)' to test the matrix."
