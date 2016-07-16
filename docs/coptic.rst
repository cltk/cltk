Coptic
******

Corpora
=======

Use ``CorpusImporter()`` or browse the `CLTK GitHub repository <https://github.com/cltk>`_ (anything beginning with ``coptic_``) to discover available Coptic corpora.

.. code-block:: python

   In [1]: from cltk.corpus.utils.importer import CorpusImporter

   In [2]: c = CorpusImporter('coptic')

   In [3]: c.list_corpora
   Out[3]: ['coptic_text_scriptorium']

