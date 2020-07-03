.. image:: https://img.shields.io/travis/cltk/cltk/master
   :alt: Travis (.org) branch
.. image:: https://img.shields.io/readthedocs/cltk
   :alt: Read the Docs
.. image:: https://img.shields.io/codecov/c/github/cltk/cltk/master
   :alt: Codecov branch
.. image:: https://img.shields.io/pypi/v/cltk
   :alt: PyPI
.. image:: https://img.shields.io/pypi/pyversions/cltk
   :alt: PyPI - Python Version
.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3445585.svg
   :target: https://doi.org/10.5281/zenodo.3445585


About
=====

The Classical Language Toolkit (CLTK) is a python library offering natural language processing (NLP) for the languages of pre–modern Eurasia.


Use
===

The CLTK's API offers a primary interface for most users' needs.

.. code-block:: python

   >>> from cltk import NLP
   >>> vitruvius = "Architecti est scientia pluribus disciplinis et variis eruditionibus ornata, quae ab ceteris artibus perficiuntur. Opera ea nascitur et fabrica et ratiocinatione."
   >>> cltk_nlp = NLP(language="lat")
   >>> cltk_doc = cltk_nlp.analyze(text=vitruvius)
   >>> cltk_doc.tokens[:5]
   ['Architecti', 'est', 'scientia', 'pluribus', 'disciplinis']
   >>> cltk_doc.words[1].string
   'est'
   >>> cltk_doc.words[1].stop
   True
   >>> cltk_doc.words[4].string
   'disciplinis'
   >>> cltk_doc.words[4].stop
   False
   >>> cltk_doc.words[4].lemma
   'disciplina'
   >>> cltk_doc.words[4].pos
   'NOUN'
   >>> cltk_doc.words[4].xpos
   'A1|grn1|casO|gen2'
   >>> cltk_doc.words[4].governor
   8
   >>> cltk_doc.words[8].string
   'ornata'
   >>> cltk_doc.words[4].dependency_relation
   'obl'
   >>> cltk_doc.words[4].embedding[:5]
   array([-0.10924 , -0.048127,  0.15953 , -0.19465 ,  0.17935 ],
         dtype=float32)


The ``NLP()`` class comes with a pre-configured processing pipeline for a number of languages (`see all here <https://cltkv1.readthedocs.io/en/latest/cltk.languages.html#module-cltk.languages.pipelines>`_). For customizing the pipeline or calling particular functions individually, see the docs.


Installation
============

.. code-block:: bash

   $ pip install cltk

To build locally: ``$ make install``


Documentation
=============

Documentation is available at `<https://docs.cltk.org>`_.

To build from this repo: ``$ make docs``, then open ``docs/_build/html/index.html``.


Tutorials
=========

Notebooks are available at `<https://github.com/cltk/tutorials>`_.


Citation
========

.. code-block::

   @Misc{johnsonetal2014,
    author = {Johnson, Kyle P. and Patrick Burns and John Stewart and Todd Cook},
    title = {CLTK: The Classical Language Toolkit},
    url = {https://github.com/cltk/cltk},
    year = {2014--2020},
   }


Development
===========

The following steps will give you a working development environment.


Python setup
------------

Use pyenv to manage Python versions and Poetry for package builds.

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
---------

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


License
=======

The CLTK is Copyright (c) 2014-2019 Kyle P. Johnson, under the MIT License. See `LICENSE <https://github.com/cltk/cltk/blob/master/LICENSE>`_.
