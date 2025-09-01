Data
====

The CLTK downloads dependency data into a directory at ``~/cltk_data``.

.. tip::

   A user can override the default location of the ``cltk_data`` directory by setting the environmental variable ``$CLTK_DATA``. E.g., ``CLTK_DATA="/opt/custom-dir"``.


Discovering and downloading
---------------------------


.. code-block:: python

   >>> from cltk.data.fetch import FetchCorpus
   >>> corpus_downloader = FetchCorpus(language="lat")
   >>> corpus_downloader.list_corpora
   ['example_distributed_latin_corpus', 'lat_text_perseus', 'lat_treebank_perseus', 'lat_text_latin_library', 'phi5', 'phi7', 'latin_proper_names_cltk', 'lat_models_cltk', 'latin_pos_lemmata_cltk', 'latin_treebank_index_thomisticus', 'latin_lexica_perseus', 'latin_training_set_sentence_cltk', 'latin_word2vec_cltk', 'latin_text_antique_digiliblt', 'latin_text_corpus_grammaticorum_latinorum', 'latin_text_poeti_ditalia', 'lat_text_tesserae']
   >>> corpus_downloader.import_corpus("lat_models_cltk")
   2020-07-04 14:48:24 INFO: Pulling latest 'lat_models_cltk' from 'https://github.com/cltk/lat_models_cltk.git'.


For a local corpus, such as the TLG, you must give a second argument of the filepath to the corpus, e.g.:

.. code-block:: python

   >>> corpus_importer.import_corpus('phi5', '~/Documents/corpora/PHI5/')


.. note::

   The CLTK depends on several libraries (Stanza, fastText) which host their own models. The CLTK will offer to download these for you.


Self-hosted corpora and models
------------------------------

Users can import any repository that is hosted on a Git server. These may be declared in \
``~/cltk_data/distributed_corpora.yaml``.

.. code-block:: python

   example_distributed_latin_corpus:
       origin: https://github.com/kylepjohnson/latin_corpus_newton_example.git
       language: latin
       type: text

   example_distributed_greek_corpus:
       origin: https://github.com/kylepjohnson/a_nonexistent_repo.git
       language: pali
       type: treebank
