build:
	poetry build

docs:
	# typed_ast crashes ``sphinx-autodoc-typehints``; is dependency of ``mypy``, however not required for py3.8 and above
	pip uninstall -y typed_ast && poetry run sphinx-apidoc --force --output-dir=docs --module-first src/cltk && cd docs && poetry run make html && cd ..

downloadAllModels:
	poetry run python scripts/download_all_models.py

format:
	poetry run isort src/cltk tests docs scripts && poetry run black src/cltk tests docs scripts

freezeDependencies:
	# Update lock file from pyptoject.toml, but do not install the changed/added packages
	poetry lock

install:
	echo "Excluding ``[tool.poetry.dev-dependencies]`` in ``pyproject.toml``"
	poetry install --no-dev

installDev:
	# Including ``[tool.poetry.dev-dependencies]`` in ``pyproject.toml``
	poetry install

installLegacy:
	# For cltk v. 0.1
	python setup.py install

installPyPI:
	poetry run pip install --pre cltk

installPyPITest:
	pip install --index-url https://test.pypi.org/simple/ --no-deps cltk

lint:
	mkdir -p pylint && poetry run pylint --output-format=json cltk > pylint/pylint.json || true && poetry run pylint-json2html pylint/pylint.json 1> pylint/pylint.html

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

test:
	echo "Going to run all tests ..."
	poetry run tox

testLatNLP:
	poetry run pytest tests/test_sanity_lat_only.py

testNoInternet:
	poetry run pytest tests/test_sanity_no_internet.py tests/test_utils.py tests/test_text.py

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
