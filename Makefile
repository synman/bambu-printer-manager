.PHONY: lint lint-fix format precommit-install help

help:
	@echo "Available targets:"
	@echo "  lint              - Run all linters on src/ (black check, isort check, flake8)"
	@echo "  lint-fix          - Run linters with auto-fix (black, isort)"
	@echo "  format            - Format code with black and isort"
	@echo "  precommit-install - Install pre-commit hooks"

lint:
	@echo "Running black check..."
	black --check src/
	@echo "Running isort check..."
	isort --check-only src/
	@echo "Running flake8..."
	flake8 src/

lint-fix: format

format:
	@echo "Formatting with black..."
	black src/
	@echo "Sorting imports with isort..."
	isort src/

precommit-install:
	@echo "Installing pre-commit hooks..."
	pre-commit install
