Sanskrit
********

Corpora
=======

Use ``CorpusImporter()`` or browse the `CLTK GitHub repository <https://github.com/cltk>`_ (anything beginning with ``sanskrit_``) to discover available Sanskrit corpora.

.. code-block:: python

   In [1]: from cltk.corpus.utils.importer import CorpusImporter

   In [2]: c = CorpusImporter('sanskrit')

   In [3]: c.list_corpora
   Out[3]:
   ['sanskrit_text_jnu', 'sanskrit_text_dcs', 'sanskrit_parallel_sacred_texts', 'sanskrit_text_sacred_texts', 'sanskrit_parallel_gitasupersite', 'sanskrit_text_gitasupersite']


