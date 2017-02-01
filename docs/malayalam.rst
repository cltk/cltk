Malayalam
********

Corpora
=======

Use ``CorpusImporter()`` or browse the `CLTK GitHub repository <https://github.com/cltk>`_ (anything beginning with ``malayalam_``) to discover available Malayalam corpora.

.. code-block:: python

   In [1]: from cltk.corpus.utils.importer import CorpusImporter

   In [2]: c = CorpusImporter('malayalam')

   In [3]: c.list_corpora
   Out[3]:
   ['malayalam_text_gretil']
