build:
	poetry build

docs:
	@echo "Building MkDocs site..."
	poetry run mkdocs build --strict

docsServe:
	@echo "Serving MkDocs site at http://127.0.0.1:8000 ..."
	poetry run mkdocs serve -a 127.0.0.1:8000

fix:
	poetry run ruff check --fix src/

format:
	poetry run ruff format src/

freezeDependencies:
	# Update lock file from pyptoject.toml, but do not install the changed/added packages
	poetry lock

install:
	poetry install --only main

installOptionals:
	poetry install -E openai
	poetry install -E stanza
	poetry install -E ollama
	poetry install -E mistral

installDev:
	poetry install

installPyPI:
	poetry run pip install --pre cltk

installPyPITest:
	pip install --index-url https://test.pypi.org/simple/ --no-deps cltk

lint:
	poetry run ruff check src/

notebook:
	poetry run jupyter notebook notebooks

preCommitUpdate:
	poetry run pre-commit autoupdate && poetry run pre-commit install --install-hooks && poetry run pre-commit autoupdate

preCommitRun:
	poetry run pre-commit run --all-files

publishPyPI:
	make build
	poetry publish

publishPyPITest:
	# poetry version prerelease
	make build
	poetry publish --repository=testpypi

publishPyPITestConfig:
	poetry config repositories.testpypi https://test.pypi.org/legacy/

shell:
	echo 'Tip: Use `option ``doctest_mode`` when making doctests'
	poetry run ipython --automagic

updateSnapshot:
	poetry run pytest -k test_public_api_snapshot --snapshot-update

testSnapshot:
	poetry run pytest -k test_public_api_snapshot --snapshot-update

test: typing
	@echo "Running tests with coverage..."
	poetry run pytest --cov=cltk --cov-report=term-missing

docstrCoverage:
	poetry run interrogate -c pyproject.toml -v src

typing:
	poetry run mypy --check-untyped-defs --html-report .mypy_cache src/cltk

uninstall:
	poetry run pip uninstall -y cltk

updateDependencies:
	poetry update

.PHONY: build docs docsServe test typing
