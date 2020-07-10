Use pyenv to manage Python versions and Poetry for package builds.

* Install ``pyenv``:
   - First time installation; ``curl https://pyenv.run | bash``
   - To update: ``pyenv update``
   - Resource: `Managing Multiple Python Versions With pyenv <https://realpython.com/intro-to-pyenv/>`_
* Install supported versions of the Python language through ``pyenv`` into a dedicated virtualenv:
   - Find the Python versions supported by the CLTK, see ``poetry.toml``.
   - ``$ pyenv install --list | grep 3.8``
   - ``$ pyenv install 3.8.3`` (or whatever is latest)
   - ``$ pyenv virtualenv 3.8.3 cltk``
   - ``$ pyenv local cltk``. Open a new window and this should be activated (check with ``$ python --version``).
* Install ``poetry`` for packaging: ``$ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python`` (`<https://poetry.eustace.io/docs/>`_)
* Install dependencies in ``poetry.lock``: ``$ poetry install``
* Install Stanford NLP models: ``$ poetry run python scripts/download_misc_dependencies.py``
* Install Graphiz (necessary for building docs): `<https://graphviz.gitlab.io/download/>`_
