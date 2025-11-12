.PHONY: help lint lint-fix format precommit-install

help:
	@echo "Available targets:"
	@echo "  lint             - Run all linters (black check, isort check, flake8)"
	@echo "  lint-fix         - Run linters and fix issues (black, isort)"
	@echo "  format           - Auto-format code with black and isort"
	@echo "  precommit-install - Install pre-commit hooks"

lint:
	@echo "Running Black (check only)..."
	black --check .
	@echo "Running isort (check only)..."
	isort --check-only .
	@echo "Running Flake8..."
	flake8 .
	@echo "Lint checks complete!"

lint-fix:
	@echo "Running Black..."
	black .
	@echo "Running isort..."
	isort .
	@echo "Running Flake8..."
	flake8 .
	@echo "Lint fixes complete!"

format:
	@echo "Formatting with Black..."
	black .
	@echo "Formatting with isort..."
	isort .
	@echo "Formatting complete!"

precommit-install:
	@echo "Installing pre-commit hooks..."
	pre-commit install
	@echo "Pre-commit hooks installed!"
