Chinese
*******

Chinese can be traced back to a hypothetical Sino-Tibetan proto-language. The first written records appeared over 3,000 years ago during the Shang dynasty. The earliest examples of Chinese are divinatory inscriptions on oracle bones from around 1250 BCE in the late Shang dynasty. Old Chinese was the language of the Western Zhou period (1046–771 BCE), recorded in inscriptions on bronze artifacts, the Classic of Poetry and portions of the Book of Documents and I Ching. Middle Chinese was the language used during Northern and Southern dynasties and the Sui, Tang, and Song dynasties (6th through 10th centuries CE). (Source: `Wikipedia <https://en.wikipedia.org/wiki/Chinese_language>`_)


Corpora
=======

Use ``CorpusImporter()`` or browse the `CLTK GitHub organization <https://github.com/cltk>`_ (anything beginning with ``chinese_``) to discover available Chinese corpora.

.. code-block:: python

   In [1]: from cltk.corpus.utils.importer import CorpusImporter

   In [2]: c = CorpusImporter('chinese')

   In [3]: c.list_corpora
   Out[3]:
   ['chinese_text_cbeta_01',
    'chinese_text_cbeta_02',
    'chinese_text_cbeta_indices']
