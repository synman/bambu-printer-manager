.PHONY: lint lint-fix format precommit-install help

help:
	@echo "Available targets:"
	@echo "  lint              - Run all linters (black check, isort check, flake8)"
	@echo "  lint-fix          - Run linters with auto-fix (black, isort)"
	@echo "  format            - Format code with black and isort"
	@echo "  precommit-install - Install pre-commit hooks"

lint:
	@echo "Running black check..."
	black --check src/ docs/
	@echo "Running isort check..."
	isort --check-only src/ docs/
	@echo "Running flake8..."
	flake8 src/ docs/

lint-fix: format

format:
	@echo "Formatting with black..."
	black src/ docs/
	@echo "Sorting imports with isort..."
	isort src/ docs/

precommit-install:
	@echo "Installing pre-commit hooks..."
	pre-commit install
