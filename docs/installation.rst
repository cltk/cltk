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

The `CLTK source is available at GitHub <https://github.com/kylepjohnson/cltk>`_. To build from source, clone the repository and make a virtual environment (as above). Then, install the CLTK with ``pip install cltk``, which will bring in all required dependencies.

If you're modifying the source, all you need to do is test your changes from within a shell (like ``python`` or ``ipython``) in the repository's root. When considering pushing your changes to the CLTK's GitHub repository, you should validate its build with the following:

.. code-block:: shell

   $ python setup.py sdist install

If you are going to make a pull request to the CLTK, also confirm that you have not broken any tests by running ``python cltk/tests/test_cltk.py``.