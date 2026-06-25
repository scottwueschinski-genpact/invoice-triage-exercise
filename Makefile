.DEFAULT_GOAL := help
PY := python3

help: ## Show this help
	@echo "Invoice Triage Exercise - available commands:"
	@echo "  make setup   Check your Python version (no packages required)"
	@echo "  make test    Run the unit tests (your build target - start here)"
	@echo "  make eval    Run the agent over the invoice batch and score it"
	@echo "  make run     Alias for 'make eval'"

setup: ## Verify the environment (Python 3.10+, standard library only)
	@$(PY) --version
	@$(PY) -c "import sys; assert sys.version_info >= (3,10), 'Need Python 3.10+'; print('Environment OK - no pip install needed.')"

test: ## Run the unit test suite
	@PYTHONPATH=src $(PY) -m unittest discover -s tests -v

eval: ## Run the agent end-to-end and score against the gold labels
	@PYTHONPATH=src $(PY) eval/run_eval.py

run: eval ## Alias for eval

.PHONY: help setup test eval run
