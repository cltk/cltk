Multilingual
*************

Corpora
=======

The CLTK uses languages in its organization of data, however some good corpora do not and cannot be easily broken apart. Furthermore, some, such as parallel text corpora, are inherently multilingual. Use ``CorpusImporter()`` or browse the `CLTK GitHub repository <https://github.com/cltk>`_ (anything beginning with ``multilingual_``) to discover available multilingual corpora.

.. code-block:: python

   In [1]: from cltk.corpus.utils.importer import CorpusImporter

   In [2]: c = CorpusImporter('multilingual')

   In [3]: c.list_corpora
   Out[3]: ['multilingual_treebank_proiel']

