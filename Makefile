SHELL := /usr/bin/env bash

build:
	uv build

docs:
	@echo "Building MkDocs site..."
	uv run mkdocs build --strict

docsServe:
	@echo "Serving MkDocs site at http://127.0.0.1:8000 ..."
	uv run mkdocs serve -a 127.0.0.1:8000

fix:
	uv run ruff check --fix src/

format:
	uv run ruff format src/ tests/ scripts/

freezeDependencies:
	# Update uv.lock from pyproject.toml without installing packages
	uv lock

install:
	uv sync --no-default-groups --frozen

installOptionals:
# 	uv sync --no-default-groups --extra openai --extra stanza --extra ollama --extra mistral --frozen
	uv sync --all-extras

installDev:
	uv sync --frozen

installPyPI:
	uv pip install --pre cltk

installPyPITest:
	pip install --index-url https://test.pypi.org/simple/ --no-deps cltk

lint:
	uv run ruff check src/

notebook:
	uv run jupyter notebook notebooks

preCommitUpdate:
	uv run pre-commit autoupdate && uv run pre-commit install --install-hooks && uv run pre-commit autoupdate

preCommitRun:
	uv run pre-commit run --all-files

publishPyPI:
	make build
	uv publish

publishPyPITest:
	make build
	uv publish --publish-url https://test.pypi.org/legacy/ --check-url https://test.pypi.org/simple

publishPyPITestConfig:
	uv publish --dry-run --publish-url https://test.pypi.org/legacy/ --check-url https://test.pypi.org/simple

shell:
	echo 'Tip: Use `option ``doctest_mode`` when making doctests'
	uv run ipython --automagic

updateSnapshot:
	uv run pytest -k test_public_api_snapshot --snapshot-update

testSnapshot:
	uv run pytest -k test_public_api_snapshot --snapshot-update

test: typing
	@echo "Running tests with coverage..."
	uv run pytest --cov=cltk --cov-report=term-missing

docstrCoverage:
	uv run interrogate -c pyproject.toml -v src

typing:
	uv run mypy --check-untyped-defs --html-report .mypy_cache src/cltk

testBuilt:
	@set -euo pipefail; \
	tmpdir=$$(mktemp -d); \
	trap 'rm -rf "$$tmpdir"' EXIT; \
	echo "Building wheel into $$tmpdir/dist ..."; \
	uv build --out-dir $$tmpdir/dist; \
	echo "Creating temp venv at $$tmpdir/venv ..."; \
	python3 -m venv $$tmpdir/venv; \
	$$tmpdir/venv/bin/python -m pip install --upgrade pip >/dev/null; \
	echo "Exporting dev requirements ..."; \
	uv export --group development --frozen --no-emit-project --no-editable > $$tmpdir/dev-requirements.txt; \
	echo "Installing development dependencies ..."; \
	$$tmpdir/venv/bin/python -m pip install -r $$tmpdir/dev-requirements.txt; \
	whl_path=$$(ls $$tmpdir/dist/cltk-*.whl); \
	echo "Installing built wheel with all extras ..."; \
	$$tmpdir/venv/bin/python -m pip install "$$whl_path[stanza,openai,mistral,ollama]"; \
	echo "Running pytest against installed wheel ..."; \
	$$tmpdir/venv/bin/python -m pytest tests

uninstall:
	uv pip uninstall -y cltk

updateDependencies:
	uv lock --upgrade

.PHONY: build docs docsServe test typing testBuilt
