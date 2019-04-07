build:
	python setup.py sdist bdist_wheel

buildDocs:
	cd docs && make doctest

check:
	twine check dist

develop:
	python setup.py sdist develop

docs:
	sphinx-apidoc -o docs cltk

install:
	python setup.py install

installPyPITest:
	pip install --index-url https://test.pypi.org/simple/ cltk

lint:
	pylint --errors-only cltk

test:
	nosetests --no-skip --with-coverage --cover-package=cltk --with-doctest

typing:
	mypy cltk

upload:
	python setup.py upload

uploadTest:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

.PHONY: build
