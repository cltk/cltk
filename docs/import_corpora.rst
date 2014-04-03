Import Corpora
**************

The CLTK works soley out of the local directory ``cltk_local``, which is created at a user's root directory. Within this are two directories, ``originals``, in which copies of outside corpora are made, and ``compiled``, in which transformed copies of the former are written.

The first step is to copy outside files into the ``originals`` directory with ``import_corpora()`` and then ``convert_tlg_txt()``.


PHI 5
=====

Import PHI 5
------------

If the PHI 5 files were located at ``/Users/kyle/Downloads/corpora/PHI5/``, then the commands would be:

.. code-block:: python

   In [1]: from cltk.corpus.common.compiler import Compile
   In [2]: c = Compile()
   In [3]: c.import_corpora('phi5', '/Users/kyle/Downloads/corpora/PHI5/')


PHI 7
=====

Import PHI 7
------------

If the PHI 7 files were located at ``/Users/kyle/Downloads/corpora/PHI7/``, then the commands would be:

.. code-block:: python

   In [1]: from cltk.corpus.common.compiler import Compile
   In [2]: c = Compile()
   In [3]: c.import_corpora('phi7', '/Users/kyle/Downloads/corpora/PHI7/')


TLG
===

Import
------

.. code-block:: python

   In [1]: from cltk.corpus.common.compiler import Compile

   In [2]: c = Compile()

   In [3]: c.import_corpora('tlg', '/Users/kyle/Downloads/corpora/TLG_E/')
 
Compile into Unicode
--------------------

This will copy files from ``originals`` into ``compiled`` and translate them from Beta Code to Unicode.

.. code-block:: python

   In [1]: from cltk.corpus.common.compiler import Compile

   In [2]: c = Compile()

   In [3]: c.convert_tlg_txt()

Make Indices
------------

The TLG comes with several indices. To build a Python dictionary of the TLG's main ``AUTHTAB.DIR``, ``make_tlg_index_file_author()`` creates a file at ``cltk_local/compiled/tlg/index_file_author.txt``.

.. code-block:: python

   In [1]: from cltk.corpus.common.compiler import Compile

   In [2]: c = Compile()

   In [3]: c.make_tlg_index_file_author()
