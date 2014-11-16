Importing Corpora
*****************

The CLTK works solely out of the local directory ``cltk_data``, which is created at a user's root directory upon initialization of the ``Compile()`` class. Within this are two directories, ``originals``, in which copies of outside corpora are made, and ``compiled``, in which transformed copies of the former are written. Also within ``cltk_data`` is ``cltk.log``, which contains all of the cltk's logging.


Greek
=====


CLTK Linguistic Data, Greek
---------------------------

The CLTK makes available some pre-trained taggers and tokenizers trained on its best data sets. To download the contents of `CLTK Greek linguistic data <https://github.com/cltk/cltk_greek_linguistic_data>`_, use these commands:

.. code-block:: python

   In [1]: from cltk.corpus.common.compiler import Compile

   In [2]: c = Compile()

   In [3]: c.import_corpus('cltk_greek_linguistic_data')


CLTK Sentence Tokenizer, Greek
------------------------------

A `pre-trained rule set <https://github.com/kylepjohnson/cltk_greek_sentence_tokenizer>`_ is available for inclusion into the CLTK for the Ancient Greek language. It can be downloaded and installed locally as follows.

.. code-block:: python

   In [1]: from cltk.corpus.common.compiler import Compile

   In [2]: c = Compile()

   In [3]: c.import_corpus('sentence_tokens_greek')

You will now have the uncompressed `greek.pickle` saved to `~/cltk_data/compiled/`.


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



Latin
=====


CLTK Linguistic Data, Latin
---------------------------

The CLTK makes available some pre-trained taggers and tokenizers trained on its best data sets. To download the contents of `CLTK Latin linguistic data <https://github.com/cltk/cltk_latin_linguistic_data>`_, use these commands:

.. code-block:: python

   In [1]: from cltk.corpus.common.compiler import Compile

   In [2]: c = Compile()

   In [3]: c.import_corpus('cltk_latin_linguistic_data')


CLTK Sentence Tokenizer, Latin
------------------------------

A `pre-trained rule set <https://github.com/kylepjohnson/cltk_latin_sentence_tokenizer>`_ is available for inclusion into the CLTK for the Latin language. The relevant rule set can be downloaded and installed locally with the following.

.. code-block:: python

   In [1]: from cltk.corpus.common.compiler import Compile

   In [2]: c = Compile()

   In [3]: c.import_corpus('sentence_tokens_latin')

You will now have the uncompressed `latin.pickle` at `~/cltk_data/compiled/`.

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


New API
=======

List corpora available for remote download or local loading:

.. code-block:: python

   In [1]: list_corpora('latin')
   Out [1]: latin_text_perseus
     latin_treebank_perseus
     latin_text_lacus_curtius
     latin_text_latin_library
     phi5
     phi7
     latin_proper_names
     cltk_linguistic_data

To download a particular corpus:

   In [2]: import_corpora('latin', 'latin_text_latin_library')
   Out [2]: ...

Not that the tlgu software can be obtained this way, too: ``import_corpora('greek', 'tlgu')``.
