black:
	black cltk

build:
	python setup.py sdist bdist_wheel

check:
	twine check dist/*

develop:
	python setup.py sdist develop

docs:
	sphinx-apidoc -f -o docs cltk && cd docs && make html && cd ..

freeze:
	pip uninstall -y cltk && pip freeze > requirements-dev.txt

install:
	python setup.py install

installPyPITest:
	pip install --index-url https://test.pypi.org/simple/ cltk

lint:
	pylint --output-format=json cltk > pylint.json || true && pylint-json2html pylint.json 1> pylint.html

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

all: black lint typing test check uml docs

.PHONY: build docs
