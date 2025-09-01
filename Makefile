build:
	poetry build

docs:
	# typed_ast crashes ``sphinx-autodoc-typehints``; is dependency of ``mypy``, however not required for py3.8 and above
	pip uninstall -y typed_ast && poetry run sphinx-apidoc --force --output-dir=docs --module-first src/cltk && cd docs && poetry run make html && cd ..

# downloadAllModels:
# 	poetry run python scripts/download_all_models.py

format:
	poetry run ruff format src/

freezeDependencies:
	# Update lock file from pyptoject.toml, but do not install the changed/added packages
	poetry lock

install:
	poetry install --only main

installDev:
	poetry install

installPyPI:
	poetry run pip install --pre cltk

installPyPITest:
	pip install --index-url https://test.pypi.org/simple/ --no-deps cltk

lint:
	poetry run ruff check src/

fix:
	poetry run ruff check --fix src

notebook:
	poetry run jupyter notebook notebooks

preCommitUpdate:
	poetry run pre-commit autoupdate && poetry run pre-commit install --install-hooks && poetry run pre-commit autoupdate

preCommitRun:
	poetry run pre-commit run --all-files

profile:
	poetry run python -m cProfile -o profile.out src/cltk/nlp.py && poetry run snakeviz profile.out

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

# test:
# 	echo "Going to run all tests ..."
# 	poetry run tox

# testChatGPT:
# 	echo "Going to test code calling ChatGPT ..."
# 	poetry run python tests/test_chatgpt.py

# testLatNLP:
# 	poetry run pytest tests/test_sanity_lat_only.py

# testNoInternet:
# 	poetry run pytest tests/test_sanity_no_internet.py tests/test_utils.py tests/test_text.py

# testOnlyDocTests:
# 	echo "Going to test only doctests ..."
# 	echo "NOTE: wordnet.py doctests have been disabled!"
# 	poetry run pytest --disable-warnings --doctest-modules --ignore=src/cltk/wordnet src/cltk/

# testOnlyTestsDir:
# 	echo "Going to test only unit tests ..."
# 	poetry run pytest --disable-warnings --ignore=src/cltk/wordnet tests

typing:
	poetry run mypy --check-untyped-defs --html-report .mypy_cache src/cltk

uninstall:
	poetry run pip uninstall -y cltk

updateDependencies:
	poetry update

uml:
	cd docs/ && poetry run pyreverse -o svg ../src/cltk/ && cd ../

all: format lint typing test uml docs

.PHONY: build docs
