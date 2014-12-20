Importing Corpora
*****************
The CLTK works solely out of the local directory ``cltk_data``, which is created at a user's root directory upon the first initialization of the ``Corpus()`` class. Within this is ``originals``, in which copies of downloaded or copied files are left, and also a directory for every language for which a corpus has been downloaded. Also within ``cltk_data`` is ``cltk.log``, which contains all of the cltk's logging.

Listing corpora
===============
To see all of the corpora available for importing, use ``list_corpora()``.
.. code-block:: python

   In [1]: from cltk.corpus.importer import Corpus

   In [2]: corpus_importer = Corpus('greek')

   In [3]: corpus_importer.list_corpora
   Out[3]:
   ['tlgu',
    'greek_text_perseus',
    'phi7',
    'tlg',
    'greek_proper_names',
    'cltk_linguistic_data',
    'greek_treebank_perseus']

Importing a corpus
==================
To download a remote corpus, use the following, for example, for the Latin Library.
.. code-block:: python

   In [1]: from cltk.corpus.importer import Corpus

   In [2]: corpus_importer = Corpus('latin')

   In [3]: corpus_importer.import_corpus('latin_text_latin_library')

For a local corpus, such as the TLG, you must give a second argument of the filepath to the corpus, e.g.:
.. code-block:: python

   In [4]: corpus_importer.import_corpus('tlg', '~/Documents/corpora/TLG_E/')
