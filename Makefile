build:
	poetry build

develop:
	python setup.py sdist develop

docs:
	poetry run sphinx-apidoc --force --output-dir=docs src/cltkv1 && cd docs && poetry run make html && cd ..

downloadDependencies:
	poetry run python scripts/download_misc_dependencies.py

format:
	isort --recursive . && poetry run black src/cltkv1 tests docs scripts

install:
	# Equivalent of ``python setup.py install``
	poetry install

installPyPITest:
	pip install --index-url https://test.pypi.org/simple/ cltk

lint:
	mkdir -p pylint && poetry run pylint --output-format=json cltkv1 > pylint/pylint.json || true && poetry run pylint-json2html pylint/pylint.json 1> pylint/pylint.html

preCommitRun:
	poetry run pre-commit autoupdate && poetry run pre-commit install && poetry run pre-commit autoupdate

shell:
	# TODO: start w/ option ``doctest_mode``
	poetry run ipython --automagic

test:
	echo "Going to run all tests ..."
	poetry run tox

testOnlyDocTests:
	echo "Going to test only doctests ..."
	poetry run pytest --disable-warnings --doctest-modules src/cltkv1/

testOnlyTestsDir:
	echo "Going to test only unit tests ..."
	poetry run pytest --disable-warnings tests

typing:
	poetry run mypy --html-report .mypy_cache src/cltkv1

updateDependencies:
	# Equivalent of ``pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U``
	poetry update

uml:
	cd docs/ && poetry run pyreverse -o png ../src/cltkv1/ && cd ../

upload:
	poetry publish

uploadTest:
	poetry publish --repository=testpypi

all: black lint typing test check uml docs

.PHONY: build docs
