Installation
************
Please note that the CLTK is built, tested, and supported only on POSIX-compliant OS (namely, Linux, Mac and the BSDs).

With Pip
========


.. note::

   The CLTK is only compatible with Python 3 on a POSIX-compatible operating system (Mac OS X, Linux, BSD, etc.).

First, you'll need a working installation of `Python 3.4 <https://www.python.org/downloads/>`_, which now includes Pip. Create a virtual environment and activate it as follows:

.. code-block:: shell

   $ pyvenv venv

   $ source venv/bin/activate

Then, install the CLTK, which automatically includes all dependencies.

.. code-block:: shell

   $ pip install cltk

Second, you will need an installation of `Git <http://git-scm.com/downloads>`_, which the CLTK uses to download and update corpora, if you want to automatically import any of the `CLTK's corpora <https://github.com/cltk/>`_. Installation of Git will depend on your operating system.


.. note::

   For a user–friendly interactive shell environment, consider trying IPython, which may be invoked with ``ipython`` or `ipython notebook`` from the command line. You may install it with ``pip install ipython``.


From source
===========
The `CLTK source is available at GitHub <https://github.com/kylepjohnson/cltk>`_. To build from source, clone the repository, make a virtual environment (as above), and finally run:

.. code-block:: shell

   $ python setup.py install

If you have modified the CLTK source, rebuild the project with this same command. If you make any changes, it is a good idea to run the test suite to ensure you did not introduce any breakage. Test with:

.. code-block:: shell

   $ python cltk/tests/test_cltk.py
