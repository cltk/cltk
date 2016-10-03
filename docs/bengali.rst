Bengali
********

Corpora
=======

Use ``CorpusImporter()`` or browse the `CLTK GitHub repository <https://github.com/cltk>`_ (anything beginning with ``bengali_``) to discover available Bengali corpora.

.. code-block:: python

   In [1]: from cltk.corpus.utils.importer import CorpusImporter

   In [2]: c = CorpusImporter('bengali')

   In [3]: c.list_corpora
   Out[3]:
   ['bengali_text_wikisource']
