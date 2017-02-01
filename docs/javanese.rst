Javanese
********

Corpora
=======

Use ``CorpusImporter()`` or browse the `CLTK GitHub organization <https://github.com/cltk>`_ (anything beginning with ``javanese_``) to discover available javanese corpora.

.. code-block:: python

   In [1]: from cltk.corpus.utils.importer import CorpusImporter

   In [2]: c = CorpusImporter('javanese')

   In [3]: c.list_corpora
   Out[3]:
   ['javanese_text_gretil']
