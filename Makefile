build:
	python setup.py sdist bdist_wheel

check:
	twine check dist/*

develop:
	python setup.py sdist develop

docs:
	sphinx-apidoc -f -o docs cltk && cd docs && make html && cd ..

install:
	python setup.py install

installPyPITest:
	pip install --index-url https://test.pypi.org/simple/ cltk

lint:
	pylint cltk

lintErrors:
	pylint --errors-only cltk

test:
	nosetests --no-skip --with-coverage --cover-erase --cover-html-dir=htmlcov --cover-html --cover-package=cltk --with-doctest

typing:
	mypy --html-report .mypy_cache cltk

uml:
	cd docs && pyreverse -o png ../cltk

upload:
	python setup.py upload

uploadTest:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

all: test lintErrors typing check uml docs

.PHONY: build docs
