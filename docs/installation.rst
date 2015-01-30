Installation
************
Please note that the CLTK is built, tested, and supported only on POSIX-compliant OS (namely, Linux, Mac and the BSDs).

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
The `CLTK source is available at GitHub <https://github.com/kylepjohnson/cltk>`_. To build from source, clone the repository, make a virtual environment (as above), and finally run:

.. code-block:: shell

   $ python setup.py sdist install

If you have modified the CLTK source, rebuild the project with this same command. If you make any changes, it is a good idea to run the test suite to ensure you did not introduce any breakage. Test with:

.. code-block:: shell

   $ nosetests
