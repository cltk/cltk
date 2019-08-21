format:
	poetry run black src/cltkv1 tests docs

build:
	poetry build

develop:
	python setup.py sdist develop

docs:
	poetry run sphinx-apidoc -f -o docs src/cltkv1 && cd docs && poetry run make html && cd ..

install:
	# Equivalent of ``python setup.py install``
	# Equivalent of ``pip install -r requirements.txt``
	poetry install

installPyPITest:
	pip install --index-url https://test.pypi.org/simple/ cltk

lint:
	mkdir pylint && poetry run pylint --output-format=json cltkv1 > pylint/pylint.json || true && poetry run pylint-json2html pylint/pylint.json 1> pylint/pylint.html

test:
	# poetry run nosetests --no-skip --with-coverage --cover-erase --cover-html-dir=htmlcov --cover-html --cover-package=cltkv1 --with-doctest
	poetry run tox

typing:
	mypy --html-report .mypy_cache cltk

updateDependencies:
	# Installs the packages installed with ``poetry add <package-name>`` and entered into ``pyproject.toml``
	# Equivalent of ``pip install -r requirements.txt``
	poetry update

uml:
	cd docs && pyreverse -o png ../cltk

upload:
	poetry publish

uploadTest:
	poetry publish --repository=testpypi

all: black lint typing test check uml docs

.PHONY: build docs
