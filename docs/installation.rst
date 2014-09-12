Installation
************

Through Pip
===========

First, you'll need a working installation of `Python 3.4 <https://www.python.org/downloads/>`_, which now includes Pip.

Next, install the nltk:

.. code-block:: python

   pip install nltk

And then a few additional packages:

.. code-block:: python

   pip install astroid gnureadline readline requests requests-toolbelt numpy

If these all install correctly, move on to the CLTK:

.. code-block:: python

   pip install cltk

From source
======

The `CLTK source is available at GitHub <https://github.com/kylepjohnson/cltk>`_. To build from source, install the above requirements as above, and then clone and run within the repository's root directory:

.. code-block:: python

   python setup.py sdist install
