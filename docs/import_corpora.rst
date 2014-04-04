Import Corpora
**************

The CLTK works solely out of the local directory ``cltk_local``, which is created at a user's root directory. Within this are two directories, ``originals``, in which copies of outside corpora are made, and ``compiled``, in which transformed copies of the former are written.

The first step is to copy outside files into the ``originals`` directory with ``import_corpora()`` and then make the corpora usable to the CLTK  with ``convert_tlg_txt()``.

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

 
Compile to Unicode & Build Indices
----------------------------------

This will copy files from ``originals`` into ``compiled`` and translate them from Beta Code to Unicode.

.. code-block:: python

   In [1]: from cltk.corpus.common.compiler import Compile

   In [2]: c = Compile()

   In [3]: c.compile_phi7_txt()

This also builds two index files, ``index_file_author.txt`` and ``index_author_works.txt``. The first index is of file names and corresponding collection's names (e.g., ``'INS0015': 'Attica [Latin]'``). The latter is made from a scan of files to gather information about the sections within a collection.

TLG
===

Import
------

.. code-block:: python

   In [1]: from cltk.corpus.common.compiler import Compile

   In [2]: c = Compile()

   In [3]: c.import_corpora('tlg', '/Users/kyle/Downloads/corpora/TLG_E/')
 
Compile to Unicode & Build Indices
--------------------

This will copy files from ``originals`` into ``compiled`` and translate them from Beta Code to Unicode.

.. code-block:: python

   In [1]: from cltk.corpus.common.compiler import Compile

   In [2]: c = Compile()

   In [3]: c.compile_tlg_txt()

This function also builds three indices, ``index_author_works.txt``, ``index_file_author.txt``, and ``index_meta.txt``, and places them at ``~/cltk_local/compiled/tlg/``. ``index_author_works.txt`` is a Python dictionary of the TLG's main ``AUTHTAB.DIR`` index. ``index_file_author.txt`` scans the compiled files and pulls out title information from each author's file. ``make_tlg_meta_index()`` is a list of indices with which the TLG comes (``LSTSCDCN.DIR``).
