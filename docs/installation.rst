Installation
============

.. note::
   We currently support Python versions ``3.7``, ``3.8``, ``3.9``.

.. note::

   The CLTK supports POSIX–compliant operating systems (Linux, Mac OS X, Windows Subsystem for Linux, etc.).
   If you use the Windows Subsystem for Linux (WSL), we recommend you upgrade to WSL2 at least,
   and install the CLTK on your *Linux filesystem*, e.g. under ``/home``.


Install via Pip:

.. code-block:: bash

   $ pip install cltk


For a pre-release version:

.. code-block::

   $ pip install --pre cltk


To install from source, clone the Git repository and run:

.. code-block::

   $ git clone https://github.com/cltk/cltk.git
   $ cd cltk/
   $ make install


See :doc:`development` for more on configuring your environment for CTLK development.
