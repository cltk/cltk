Installation
************

Through Pip
===========

First, you'll need a working installation of `Python 3.4 <https://www.python.org/downloads/>`_, which now includes Pip.

Next, install the `alpha version of the NLTK (3.0a3) <http://nltk.org/nltk3-alpha/>`_:

.. code-block:: python

   pip install http://nltk.org/nltk3-alpha/nltk-3.0a3.tar.gz

.. code-block:: python

   pip install astroid gnureadline readline requests requests-toolbelt numpy

If these all install correctly, move onto the CLTK:

.. code-block:: python

   pip install cltk

Source
======

The `CLTK source is available at GitHub <https://github.com/kylepjohnson/cltk>`_. To build from source, clone and run within the repository's root directory:

.. code-block:: python

   python setup.py sdist install
