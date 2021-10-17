Development
===========

The following steps will give you a working development environment as the maintainers have.

Git
---

Begin by forking the ``cltk/cltk`` repo into your github account.

* ``$ git clone https://github.com/your-username/cltk.git``
* ``$ cd cltk``
* ``$ git remote add upstream https://github.com/cltk/cltk.git``

Python
------

Use pyenv to manage Python versions and Poetry for package builds.  Note that pyenv does not depend on Python itself.

* Install ``pyenv``:
   - First time installation; ``curl https://pyenv.run | bash``
   - Resource: `Managing Multiple Python Versions With pyenv <https://realpython.com/intro-to-pyenv/>`_
* Install supported versions of the Python language through ``pyenv`` into a dedicated virtualenv:
   - Find the Python versions supported by the CLTK, see ``pyproject.toml``.
   - ``$ pyenv install --list | grep 3.8``
   - ``$ pyenv install 3.8.3`` (or whatever is latest)
   - ``$ pyenv virtualenv 3.8.3 cltk``.
   - Ensure that your working directory is ``cltk``, then: ``$ pyenv local cltk``. Open a new terminal and this should be activated (check with ``$ python --version``).
* Install ``poetry`` for packaging: ``$ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python`` (`<https://poetry.eustace.io/docs/>`_)
* Install dependencies in ``poetry.lock``: ``$ poetry install``
* Download NLP models: ``$ poetry run python scripts/download_all_models.py`` with optional flag ``--languages=lat`` for only those of a specific language.
* Install Graphiz (necessary for building docs): `<https://graphviz.gitlab.io/download/>`_


Git Flow
--------

* ``$ git checkout -b fix-feature``
* Do changes
* Install: ``$ make install``
* Check changes in interactive Python shell (``$ make shell``) or notebook (``$ make notebook``)
* Run doctests locally: ``$ make testOnlyDocTests``
* ``$ make docs``. Check that the docs look good for any modules you changed: ``docs/_build/html/index.html``.
* ``$ git push origin fix-feature``
* Open pull request: `<https://github.com/your-username/cltk/pull/new/master>`_
* Wait for Travis CI to report build success for your PR: `<https://travis-ci.org/github/cltk/cltk/pull_requests>`_. Confirm code coverage and docs build OK, too.
* A maintainer will review your code and either request changes or accept.
* Once accepted, a maintainer will package a new version and publish it to PyPI (`Packaging`_).
* After the PR is accepted and version incremented, update your local repo:
   - ``$ git checkout master``
   - ``$ git pull upstream master``
   - ``$ git push origin master``


Packaging
---------

* Validate structure of ``pyproject.toml``: ``$ poetry check``
* Update project version with ``poetry``:
   - For pre-release: ``$ poetry version prerelease`` (e.g., ``1.0.0`` to ``1.0.0-alpha.0``)
   - For patch: ``$ poetry version prepatch`` (e.g., ``1.0.0`` to ``1.0.1-alpha.0``)
   - For minor version: ``$ poetry version preminor`` (``1.0.0`` to ``1.1.0-alpha.0``)
   - For major version: ``$ poetry version premajor`` (``1.0.0`` to ``2.0.0-alpha.0``)
* Update all dependencies to latest version (optional): ``$ make updateDependencies``
   - Poetry will not automatically update major versions (e.g., ``2.x`` to ``1.x``), even if the ``pyproject.toml`` is ``"^1.3"``. To view new major releases, use ``$ poetry show -o``. You would then need to manually update the config file to the latest.
   - Only maintainers should do dependency updates, unless an upgrade is required by a contributor.
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
* Run config check: ``$ make publishPyPITestConfig``
* Publish pre-release (permissions required): ``$ make publishPyPITest``
* Install from TestPyPI: ``$ make installPyPITest``
* Repeat the above as necessary
* Bump version: ``$ poetry version patch`` (e.g., ``1.0.1-alpha.0`` to ``1.0.1``)
   - For minor version: ``$ poetry version minor`` (``1.0.1-alpha.0`` to ``1.1.0``)
   - For major version: ``$ poetry version major`` (``1.0.1-alpha.0`` to ``2.0.0``)
   - If you need to publish multiple versions of an alpha pre-release, run ``$ poetry version prerelease`` (e.g., ``1.0.1-alpha.0`` to ``1.0.1-alpha.1`` to ``1.0.1-alpha.2``)
* Publish to PyPI (permissions required): ``$ make publishPyPI``
