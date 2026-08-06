help:
	@echo "targets:"
	@echo "test:       Run all tests"
	@echo "coverage:   Run tests with a coverage report"
	@echo "format:     Format the code"
	@echo "check:      Lint the code"
	@echo "check-fix:  Lint the code and apply safe fixes"
	@echo "typecheck:  Run mypy"
	@echo "docs:       Build the documentation site"
	@echo "docs-serve: Serve the documentation with live reload"
	@echo "all:        Run every check the CI runs"
	@echo "help:       Show this help"

test:
	poetry run pytest -vvv

coverage:
	poetry run pytest -vvv --cov=shadow_data --cov-report=term-missing

format:
	poetry run ruff format .

check:
	poetry run ruff check .

check-fix:
	poetry run ruff check --fix .

typecheck:
	poetry run mypy

docs:
	poetry run mkdocs build --strict

docs-serve:
	poetry run mkdocs serve

all: check typecheck docs
	poetry run ruff format --check .
	poetry run pytest -vvv --cov=shadow_data --cov-fail-under=90

.PHONY: help test coverage format check check-fix typecheck docs docs-serve all

