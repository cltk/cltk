Hebrew
******

Hebrew is a language native to Israel, spoken by over 9 million people worldwide, of whom over 5 million are in Israel. Historically, it is regarded as the language of the Israelites and their ancestors, although the language was not referred to by the name Hebrew in the Tanakh. The earliest examples of written Paleo-Hebrew date from the 10th century BCE. Hebrew belongs to the West Semitic branch of the Afroasiatic language family. The Hebrew language is the only living Canaanite language left. Hebrew had ceased to be an everyday spoken language somewhere between 200 and 400 CE, declining since the aftermath of the Bar Kokhba revolt. (Source: `Wikipedia <https://en.wikipedia.org/wiki/Hebrew_language>`_)


Corpora
=======

Use ``CorpusImporter`` or browse the `CLTK Github repository <http://github.com/cltk>`_ (anything beginning with ``hebrew_``) to discover available Hebrew corpora.

.. code-block:: python

   In [1]: from cltk.corpus.utils.importer import CorpusImporter
   In [2]: corpus_importer = CorpusImporter('hebrew')
   In [3]: corpus_importer.list_corpora
   Out[3]:
   ['hebrew_text_sefaria']


Alphabet
========

The Hebrew alphabet and digits are placed in `cltk/corpus/hebrew/alphabet.py <https://github.com/cltk/cltk/blob/master/cltk/corpus/hebrew/alphabet.py>`_.

The digits are placed in a list ``DIGITS`` with the digit in the following order (None,1,...18,19,20,30,40,50,60......90,100,200,300.....900,1000,2000,5000,10000,100000,1000000).There is no alphabet for digit 0. For example, the hebrew digit for 4 can be accessed in this manner:

.. code-block:: python

   In [1]: from cltk.corpus.hebrew.alphabet import DIGITS
   In [2]: DIGITS[4]
   Out[2]: 'ד'

The entire list of alphabets can be accessed in this manner:

.. code-block:: python

   In [1]: from cltk.corpus.hebrew.alphabet import ALPHABET
   In [2]: ALPHABET
   Out[2]: ['ז', 'ו', 'ה', 'ד', 'ג', 'בּ/ב', 'א', 'מ', 'ל', 'ך', 'כּ/כ', 'י', 'ט', 'ח', 'ף', 'פּ/פ', 'ע', 'ס', 'ן', 'נ', 'ם', 'ת', 'שׁ/שׂ', 'ר', 'ק', 'ץ', 'צ', "'ת", "'צ", "'ע", "'ח", "'ז", "'ד", "'ג"] 

The list of vowels can be accessed in this manner:

.. code-block:: python

   In [1]: from cltk.corpus.hebrew.alphabet import VOWELS
   In [2]: VOWELS
   Out[2]: ['אְ', 'אִ', 'אֵ', 'אֶ', 'אָ', 'אַ', 'ׂא', 'וֹ', 'אֻ', 'וּ', 'תּ', 'שׁ', 'שׂ', 'אֱ', 'אֲ', "אֳ"]



