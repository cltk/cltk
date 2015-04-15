Tibetan
*******

Corpora
=======

Use ``CorpusImporter()`` or browse the `CLTK GitHub repository <https://github.com/cltk>`_ (anything beginning with ``tibetan_``) to discover available Tibetan corpora.

.. code-block:: python

   In [1]: from cltk.corpus.utils.importer import CorpusImporter

   In [2]: c = CorpusImporter('tibetan')

   In [3]: c.list_corpora
   Out[3]: ['tibetan_pos_tdc', 'tibetan_lexica_tdc']

