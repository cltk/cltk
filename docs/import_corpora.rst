Import Corpora
**************

The CLTK works solely out of the local directory ``cltk_local``, which is created at a user's root directory. Within this are two directories, ``originals``, in which copies of outside corpora are made, and ``compiled``, in which transformed copies of the former are written.


Latin
=====

PHI 5
-----

If the PHI 5 files were located at ``/Users/kyle/Downloads/corpora/PHI5/``, then the commands would be:

.. code-block:: python

   In [1]: from cltk.corpus.common.compiler import Compile
   In [2]: c = Compile()
   In [3]: c.import_corpora('phi5', '/Users/kyle/Downloads/corpora/PHI5/')

In addition to copying the PHI5's author files at ``~/cltk_local/compiled/phi5/``, it creates ``index_author_works.txt`` and ``index_file_author.txt``.

PHI 7
-----
See instructions under Classical Greek.


Classical Greek
===============

PHI 7
-----

If the PHI 7 files were located at ``/Users/kyle/Downloads/corpora/PHI7/``, then the commands would be:

.. code-block:: python

   In [1]: from cltk.corpus.common.compiler import Compile
   In [2]: c = Compile()
   In [3]: c.import_corpora('phi7', '/Users/kyle/Downloads/corpora/PHI7/')

In addition to copying the PHI7's author files at ``~/cltk_local/compiled/phi7/``, it creates ``index_author_works.txt`` and ``index_file_author.txt``.

TLG
---

.. code-block:: python

   In [1]: from cltk.corpus.common.compiler import Compile

   In [2]: c = Compile()

   In [3]: c.import_corpora('tlg', '/Users/kyle/Downloads/corpora/TLG_E/')


In addition to copying the TLG's author files at ``~/cltk_local/compiled/tlg/``, it creates ``index_author_works.txt``, ``index_file_author.txt``,  and ``index_meta.txt`` (an index of the TLG's other indices).
