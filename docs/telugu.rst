Telugu
********

Corpora
=======

Use ``CorpusImporter()`` or browse the `CLTK GitHub repository <https://github.com/cltk>`_ (anything beginning with ``telugu_``) to discover available Telugu corpora.

.. code-block:: python

   In [1]: from cltk.corpus.utils.importer import CorpusImporter

   In [2]: c = CorpusImporter('telugu')

   In [3]: c.list_corpora
   Out[3]:
   ['telugu_text_wikisource']
