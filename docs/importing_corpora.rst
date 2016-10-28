Importing Corpora
*****************
The CLTK stores all data in the local directory ``cltk_data``, which is created at a user's root directory upon first initialization of the ``CorpusImporter()`` class. Within this are an ``originals`` directory, in which untouched copies of downloaded or copied files are preserved, and a directory for every language for which a corpus has been downloaded. It also contains ``cltk.log`` for all CLTK logging.

Listing corpora
===============
To see all of the corpora available for importing, use ``list_corpora()``.

.. code-block:: python

   In [1]: from cltk.corpus.utils.importer import CorpusImporter

   In [2]: corpus_importer = CorpusImporter('greek')  # e.g., or CorpusImporter('latin')

   In [3]: corpus_importer.list_corpora

   Out[3]:
   ['greek_software_tlgu',
    'greek_text_perseus',
    'phi7',
    'tlg',
    'greek_proper_names_cltk',
    'greek_models_cltk',
    'greek_treebank_perseus',
    'greek_lexica_perseus',
    'greek_training_set_sentence_cltk',
    'greek_word2vec_cltk',
    'greek_text_lacus_curtius']


Importing a corpus
==================
To download a remote corpus, use the following, for example, for the Latin Library.

.. code-block:: python

   In [1]: from cltk.corpus.utils.importer import CorpusImporter

   In [2]: corpus_importer = CorpusImporter('latin')  # e.g., or CorpusImporter('greek')

   In [3]: corpus_importer.import_corpus('latin_text_latin_library')
   Downloaded 100% , 35.53 MiB | 3.28 MiB/s s

For a local corpus, such as the TLG, you must give a second argument of the filepath to the corpus, e.g.:

.. code-block:: python

   In [4]: corpus_importer.import_corpus('tlg', '~/Documents/corpora/TLG_E/')


User-defined, distributed corpora
=================================

Most users will want to use the CLTK's publicly available corpora. However users can import any repository \
that is hosted on a Git server. The benefit of this is that users can use corpora \
that the CLTK organization is not able to distribute itself (because too specific, license restrictions, etc.).

Let's say a user wants to keep a particular Git-backed corpus at \
``git@github.com:kylepjohnson/latin_corpus_newton_example.git``. It can be cloned \
into the ``~/cltk_data/`` directory by declaring it in a manually created YAML file at \
``~/cltk_data/distributed_corpora.yaml`` like the following:

.. code-block:: python

   example_distributed_latin_corpus:
       origin: git@github.com:kylepjohnson/latin_corpus_newton_example.git
       language: latin
       type: text

   example_distributed_greek_corpus:
       origin: git@github.com:kylepjohnson/a_nonexistent_repo.git
       language: pali
       type: treebank

Each block defines a separate corpus. The first line of a block (e.g., ``example_distributed_latin_corpus``) \
gives the unique name to the custom corpus, however it is not used elsewhere. This first example block would allow \
a user to fetch the repo and install it at ``~/cltk_data/latin/text/latin_corpus_newton_example``.