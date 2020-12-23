build:
	poetry build

develop:
	python setup.py sdist develop

docs:
	# typed_ast crashes ``sphinx-autodoc-typehints``; is dependency of ``mypy``, however not required for py3.8 and above
	pip uninstall -y typed_ast && poetry run sphinx-apidoc --force --output-dir=docs --module-first src/cltk && cd docs && poetry run make html && cd ..

downloadDependencies:
	poetry run python scripts/download_all_models.py

format:
	poetry run isort --recursive . && poetry run black src/cltk tests docs scripts

install:
	poetry install

installPyPI:
	poetry run pip install --pre cltk

installPyPITest:
	pip install --index-url https://test.pypi.org/simple/ --no-deps cltk

lint:
	mkdir -p pylint && poetry run pylint --output-format=json cltk > pylint/pylint.json || true && poetry run pylint-json2html pylint/pylint.json 1> pylint/pylint.html

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
	# TODO: start w/ option ``doctest_mode``
	poetry run ipython --automagic

test:
	echo "Going to run all tests ..."
	poetry run tox

testOnlyDocTests:
	echo "Going to test only doctests ..."
	echo "NOTE: wordnet.py doctests have been disabled!"
	poetry run pytest --disable-warnings --doctest-modules --ignore=src/cltk/wordnet src/cltk/

testOnlyTestsDir:
	echo "Going to test only unit tests ..."
	echo "NOTE: wordnet.py doctests have been disabled!"
	poetry run pytest --disable-warnings --ignore=src/cltk/wordnet tests

typing:
	poetry run mypy --html-report .mypy_cache src/cltk

uninstall:
	poetry run pip uninstall -y cltk

updateDependencies:
	poetry update

uml:
	cd docs/ && poetry run pyreverse -o svg ../src/cltk/ && cd ../

all: format lint typing test uml docs

.PHONY: build docs
