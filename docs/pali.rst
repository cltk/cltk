Pali
****

Corpora
=======

Use ``CorpusImporter()`` or browse the `CLTK GitHub repository <https://github.com/cltk>`_ (anything beginning with ``pali_``) to discover available Pali corpora.

.. code-block:: python

   In [1]: from cltk.corpus.utils.importer import CorpusImporter

   In [2]: c = CorpusImporter('pali')

   In [3]: c.list_corpora
   Out[3]: ['pali_text_ptr_tipitaka']

