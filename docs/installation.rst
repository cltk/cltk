Installation
************

With Pip
========

First, you'll need a working installation of `Python 3.4 <https://www.python.org/downloads/>`_, which now includes Pip. Create a virtual environment and activate it as follows:

.. code-block:: shell

   $ pyvenv venv

   $ source venv/bin/activate

Then, install the CLTK, which automatically includes all dependencies.

.. code-block:: shell

   pip install cltk

From source
===========

The `CLTK source is available at GitHub <https://github.com/kylepjohnson/cltk>`_. To build from source, install the above requirements as above, and then clone and run within the repository's root directory:

.. code-block:: shell

   python setup.py sdist install
