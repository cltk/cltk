Installation
************

Through Pip
===========

You'll need a working installation of Python 3.3 with `Pip installed alongside Python 3.3 <http://www.pip-installer.org/en/latest/installing.html>`_.

First, you'll need `the alpha version of the NLTK <http://nltk.org/nltk3-alpha/>`_::

   pip install http://nltk.org/nltk3-alpha/nltk-3.0a3.tar.gz

The CLTK is `available at PyPI <https://pypi.python.org/pypi/cltk>`_, which means that it may be installed with the following::

   pip install cltk

By source
======

`The source is available at GitHub <https://github.com/kylepjohnson/cltk>`_. To build from source, run within the root directory::

   python setup.py sdist install
