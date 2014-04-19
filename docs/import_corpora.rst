Import Corpora
**************

The CLTK works solely out of the local directory ``cltk_data``, which is created at a user's root directory. Within this are two directories, ``originals``, in which copies of outside corpora are made, and ``compiled``, in which transformed copies of the former are written.


Classical Greek
===============


Perseus Digital Library, Greek
------------------------------

A pre--compiled version of the `Perseus Digital Library  <http://www.perseus.tufts.edu/hopper/opensource/download>`_ is maintained on `GitHub <https://github.com/kylepjohnson/corpus_perseus_greek>`_. The CLTK can fetch these files with:

.. code-block:: python

   In [1]: from cltk.corpus.common.compiler import Compile

   In [2]: c = Compile()

   In [3]: c.import_corpus('perseus_greek')


Perseus Digital Library, Greek Treebank
------------------------------
A pre--compiled version of the `Perseus Digital Library's Greek treebank  <http://nlp.perseus.tufts.edu/syntax/treebank/greek.html>`_ is maintained on `GitHub <https://github.com/kylepjohnson/treebank_perseus_greek>`_. The CLTK can fetch these files with:

.. code-block:: python

   In [1]: from cltk.corpus.common.compiler import Compile

   In [2]: c = Compile()

   In [3]: c.import_corpus('treebank_perseus_greek')


PHI 7, Classical Greek
----------------------

If the PHI 7 files were located at ``/Users/kyle/Downloads/corpora/PHI7/``, then the commands would be:

.. code-block:: python

   In [1]: from cltk.corpus.common.compiler import Compile
   In [2]: c = Compile()
   In [3]: c.import_corpus('phi7', '/Users/kyle/Downloads/corpora/PHI7/')

In addition to copying the PHI7's author files at ``~/cltk_data/compiled/phi7/``, it creates ``index_author_works.txt`` and ``index_file_author.txt``.

TLG
---

.. code-block:: python

   In [1]: from cltk.corpus.common.compiler import Compile

   In [2]: c = Compile()

   In [3]: c.import_corpus('tlg', '/Users/kyle/Downloads/corpora/TLG_E/')

In addition to copying the TLG's author files at ``~/cltk_data/compiled/tlg/``, it creates ``index_author_works.txt``, ``index_file_author.txt``,  and ``index_meta.txt`` (an index of the TLG's other indices).



Classical Latin
===============

Latin Library
-------------

A pre--compiled version of the `Latin Library  <http://www.thelatinlibrary.com/>`_ is maintained on `GitHub <https://github.com/kylepjohnson/corpus_latin_library>`_. The CLTK can fetch these files with:

.. code-block:: python

   In [1]: from cltk.corpus.common.compiler import Compile

   In [2]: c = Compile()

   In [3]: c.import_corpus('latin_library')

Perseus Digital Library, Latin
------------------------------

A pre--compiled version of the `Perseus Digital Library  <http://www.perseus.tufts.edu/hopper/opensource/download>`_ is maintained on `GitHub <https://github.com/kylepjohnson/corpus_perseus_latin>`_. The CLTK can fetch these files with:

.. code-block:: python

   In [1]: from cltk.corpus.common.compiler import Compile

   In [2]: c = Compile()

   In [3]: c.import_corpus('perseus_latin')


Perseus Digital Library, Latin Treebank
------------------------------
A pre--compiled version of the `Perseus Digital Library's Latin treebank  <http://nlp.perseus.tufts.edu/syntax/treebank/latin.html>`_ is maintained on `GitHub <https://github.com/kylepjohnson/treebank_perseus_latin>`_. The CLTK can fetch these files with:

.. code-block:: python

   In [1]: from cltk.corpus.common.compiler import Compile

   In [2]: c = Compile()

   In [3]: c.import_corpus('treebank_perseus_latin')


PHI 5
-----

If the PHI 5 files were located at ``/Users/kyle/Downloads/corpora/PHI5/``, then the commands would be:

.. code-block:: python

   In [1]: from cltk.corpus.common.compiler import Compile
   In [2]: c = Compile()
   In [3]: c.import_corpus('phi5', '/Users/kyle/Downloads/corpora/PHI5/')

In addition to copying the PHI5's author files at ``~/cltk_data/compiled/phi5/``, it creates ``index_author_works.txt`` and ``index_file_author.txt``.

PHI 7, Latin
------------
See instructions under Classical Greek.


POS Tagging
-----------

Download these files for POS tagging by the CLTK.

.. code-block:: python

   In [1]: from cltk.corpus.common.compiler import Compile

   In [2]: c = Compile()

   In [3]: c.import_corpus('pos_latin')
