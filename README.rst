.. image:: https://travis-ci.org/cltk/cltkv1.svg?branch=master
    :target: https://travis-ci.org/cltk/cltkv1

About
-----

Experimental version of CLTK to incorporate stanfordnlp into an all-use ``NLP()`` class.


Development
-----------

The following steps will give you a working development environment.

Python setup
============

Setup `pyenv` and `poetry` to manage Python versions.

* Install ``pyenv``: `Managing Multiple Python Versions With pyenv <https://realpython.com/intro-to-pyenv/>`_
* ``$ pyenv virtualenv 3.7.5 cltk``
* ``$ pyenv local cltk``
* Install ``poetry``: https://poetry.eustace.io/docs/
* Install dependencies in ``poetry.lock``: ``$ poetry install``
* Install Graphiz (for building docs): https://graphviz.gitlab.io/download/

Packaging
=========

* Validate structure of ``pyproject.toml``: ``$ poetry check``
* Update project version with ``poetry``: ``$ poetry version prepatch`` (e.g., ``1.0.0`` to ``1.0.1-alpha.0``)
   - For minor version: ``$ poetry version preminor`` (``1.0.0`` to ``1.1.0-alpha.0``)
   - For major version: ``$ poetry version premajor`` (``1.0.0`` to ``2.0.0-alpha.0``)
* Update all dependencies to latest version (optional): ``$ poetry update``
* Make package (sdist and wheel): ``$ poetry build``
* Check typing: ``$ poetry run mypy --html-report .mypy_cache src/cltkv1/``
   - View report at ``.mypy_cache/index.html``
* Run linter: ``$ mkdir pylint && poetry run pylint --output-format=json cltkv1 > pylint/pylint.json || true && poetry run pylint-json2html pylint/pylint.json 1> pylint/pylint.html``
   - View report at ``pylint/pylint.html``
* Auto-format code: ``$ poetry run isort --recursive . && poetry run black src/cltkv1/ tests docs``
* Build docs: ``$ poetry run sphinx-apidoc -f -o docs src/cltkv1/ && cd docs/ && poetry run make html && cd ../``
   - View docs at ``docs/_build/html/index.html``
* Make UML diagrams: ``$ cd docs/ && poetry run pyreverse -o png ../src/cltkv1/ && cd ../``
   - View diagrams at ``docs/classes.png`` and ``docs/packages.png``
* Run tests: ``$ tox``
* Publish pre-release (permissions required): ``$ poetry publish --repository=testpypi``
* Install from TestPyPI: ``$ pip install --pre --index-url https://test.pypi.org/simple/ cltkv1``
* Repeat the above as necessary
* Bump version: ``$ poetry version patch`` (e.g., ``1.0.1-alpha.0`` to ``1.0.1``)
   - For minor version: ``$ poetry version minor`` (``1.0.1-alpha.0`` to ``1.1.0``)
   - For major version: ``$ poetry version major`` (``1.0.1-alpha.0`` to ``2.0.0``)
   - If you need to publish multiple versions of an alpha pre-release, run ``$ poetry version prerelease`` (e.g., ``1.0.1-alpha.0`` to ``1.0.1-alpha.1`` to ``1.0.1-alpha.2``)
* Publish to PyPI (permissions required): ``$ poetry publish``
