Chinese
*******
Chinese is a group of related, but in many cases mutually unintelligible, language varieties, forming a branch of the Sino-Tibetan language family. Chinese is spoken by the Han majority and many other ethnic groups in China. Nearly 1.2 billion people (around 16% of the world's population) speak some form of Chinese as their first language.

The varieties of Chinese are usually described by native speakers as dialects of a single Chinese language, but linguists note that they are as diverse as a language family.The internal diversity of Chinese has been likened to that of the Romance languages, but may be even more varied. There are between 7 and 13 main regional groups of Chinese (depending on classification scheme), of which the most spoken by far is Mandarin (about 960 million), followed by Wu (80 million), Min (70 million), and Yue (60 million).
SOURCE:`Wikipedia <https://en.wikipedia.org/wiki/Chinese_language>`_




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

