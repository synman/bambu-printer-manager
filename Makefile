.PHONY: help lint lint-fix format precommit-install check-black check-isort check-flake8 check-pylint

help:
	@echo "Available targets:"
	@echo "  lint              - Run all linting checks (black, isort, flake8)"
	@echo "  lint-fix          - Auto-fix linting issues (black, isort)"
	@echo "  format            - Format code with black and isort"
	@echo "  check-black       - Check code formatting with black"
	@echo "  check-isort       - Check import sorting with isort"
	@echo "  check-flake8      - Run flake8 linter"
	@echo "  check-pylint      - Run pylint (optional, more verbose)"
	@echo "  precommit-install - Install pre-commit hooks"

# Check code formatting
check-black:
	black --check --diff src/

# Check import sorting
check-isort:
	isort --check-only --diff src/

# Run flake8
check-flake8:
	flake8 src/

# Run pylint (optional)
check-pylint:
	pylint src/bpm/ || true

# Run all linting checks
lint: check-black check-isort check-flake8
	@echo "All linting checks passed!"

# Auto-fix linting issues
lint-fix: format
	@echo "Code formatted!"

# Format code with black and isort
format:
	black src/
	isort src/

# Install pre-commit hooks
precommit-install:
	pre-commit install
	@echo "Pre-commit hooks installed!"
