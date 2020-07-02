.. image:: https://travis-ci.org/cltk/cltk.svg?branch=master
    :target: https://travis-ci.org/cltk/cltk

About
-----

Experimental CLTK with new ``NLP()`` class.

Installation
------------

.. code-block:: bash

   $ pip install cltk


Documentation
-------------

``$ make docs``


Development
-----------

The following steps will give you a working development environment.

Python setup
============

Use ``pyenv`` to manage Python versions and ``poetry`` for package builds.

* Install ``pyenv``:
   - First time installation; ``curl https://pyenv.run | bash``
   - To update: ``pyenv update``
   - Resource: `Managing Multiple Python Versions With pyenv <https://realpython.com/intro-to-pyenv/>`_
* Install supported versions of the Python language through ``pyenv`` into a dedicated virtualenv:
   - ``$ pyenv install --list | grep 3.8``
   - ``$ pyenv install 3.8.3`` (or whatever is latest)
   - ``$ pyenv virtualenv 3.8.3 cltk``
   - ``$ pyenv local cltk``. Open a new window and this should be activated (check with ``$ python --version``).
* Install ``poetry`` to support packaging: ``$ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python`` (`<https://poetry.eustace.io/docs/>`_)
* Install dependencies in ``poetry.lock``: ``$ poetry install``
* Install Stanford NLP models: ``$ poetry run python scripts/download_misc_dependencies.py``
* Install Graphiz (necessary for building docs): https://graphviz.gitlab.io/download/


Packaging
=========

* Validate structure of ``pyproject.toml``: ``$ poetry check``
* Update project version with ``poetry``: ``$ poetry version prepatch`` (e.g., ``1.0.0`` to ``1.0.1-alpha.0``)
   - For minor version: ``$ poetry version preminor`` (``1.0.0`` to ``1.1.0-alpha.0``)
   - For major version: ``$ poetry version premajor`` (``1.0.0`` to ``2.0.0-alpha.0``)
* Update all dependencies to latest version (optional): ``$ make updateDependencies``
* Make package (sdist and wheel): ``$ make build``
* Check typing: ``$ make typing``
   - View report at ``.mypy_cache/index.html``
* Run linter: ``$ make lint``
   - View report at ``pylint/pylint.html``
* Auto-format code: ``$ make format``
* Build docs: ``$ make docs``
   - View docs at ``docs/_build/html/index.html``
* Make UML diagrams: ``$ make uml``
   - View diagrams at ``docs/classes.png`` and ``docs/packages.png``
* Run the above at each commit  with ``pre-commit``: ``$ poetry run pre-commit install`` (just once)
* Run tests: ``$ make test``
* Publish pre-release (permissions required): ``$ make uploadTest``
* Install from TestPyPI: ``$ make installPyPITest``
* Repeat the above as necessary
* Bump version: ``$ poetry version patch`` (e.g., ``1.0.1-alpha.0`` to ``1.0.1``)
   - For minor version: ``$ poetry version minor`` (``1.0.1-alpha.0`` to ``1.1.0``)
   - For major version: ``$ poetry version major`` (``1.0.1-alpha.0`` to ``2.0.0``)
   - If you need to publish multiple versions of an alpha pre-release, run ``$ poetry version prerelease`` (e.g., ``1.0.1-alpha.0`` to ``1.0.1-alpha.1`` to ``1.0.1-alpha.2``)
* Publish to PyPI (permissions required): ``$ make upload``
