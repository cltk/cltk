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

   $ pip install cltk

From source
===========

The `CLTK source is available at GitHub <https://github.com/kylepjohnson/cltk>`_. To build from source, clone the repository, make a virtual environment (as above), and install Python requirements with the following:

.. code-block:: shell

   $ pip install -r requirements.txt

If you make changes to the CLTK's source, and would like to validate them by bundling the software yourself, run the following:

.. code-block:: shell

   $ python setup.py sdist install

If you are going to make a pull request to the CLTK, consider first making a test build in this fashion and running the tests (``python cltk/tests/test_cltk.py``).