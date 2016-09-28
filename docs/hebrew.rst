Hebrew
******

Corpora
=======

Use ``CorpusImporter`` or browse the `CLTK Github repository <http://github.com/cltk>`_ (anything beginning with ``hebrew_``) to discover available Hebrew corpora.

.. code-block:: python

   In [1]: from cltk.corpus.utils.importer import CorpusImporter
   In [2]: c = CorpusImporter('hebrew')
   In [3]: c.list_corpora
   Out[3]:
   ['hebrew_text_sefaria']

