Chinese
*******
Chinese is a group of related, but in many cases mutually unintelligible, language varieties, forming a branch of the Sino-Tibetan language family. Chinese is spoken by the Han majority and many other ethnic groups in China. Nearly 1.2 billion people (around 16% of the world's population) speak some form of Chinese as their first language. Standard Chinese is a standardized form of spoken Chinese based on the Beijing dialect of Mandarin. It is the official language of China and Taiwan, as well as one of four official languages of Singapore. It is one of the six official languages of the United Nations. The written form of the standard language, based on the logograms known as Chinese characters , is shared by literate speakers of otherwise unintelligible dialects. (Source:`Wikipedia <https://en.wikipedia.org/wiki/Chinese_language>`_)

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
