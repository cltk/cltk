Tamil
*****

Tamil is a Dravidian language predominantly spoken by the Tamil people of India and Sri Lanka. It is one of the longest-surviving classical languages in the world. A recorded Tamil literature has been documented for over 2000 years. The earliest period of Tamil literature, Sangam literature, is dated from ca. 300 BC – AD 300. It has the oldest extant literature among Dravidian languages. The earliest epigraphic records found on rock edicts and hero stones date from around the 3rd century BC. More than 55% of the epigraphical inscriptions (about 55,000) found by the Archaeological Survey of India are in the Tamil language. Tamil language inscriptions written in Brahmi script have been discovered in Sri Lanka, and on trade goods in Thailand and Egypt. (Source: `Wikipedia <https://en.wikipedia.org/wiki/Tamil_language>`_)


Alphabet
=========

.. code-block:: python

   In [1]: from cltk.corpus.tamil.alphabet import VOWELS, CONSTANTS, GRANTHA_CONSONANTS

   In [2]: print(VOWELS)
   Out[2]: ['அ', 'ஆ', 'இ', 'ஈ', 'உ', 'ஊ',' எ', 'ஏ', 'ஐ', 'ஒ', 'ஓ', 'ஔ']
   
   In [3]: print(CONSONANTS)
   Out[3]: ['க்', 'ங்', 'ச்', 'ஞ்', 'ட்', 'ண்', 'த்', 'ந்', 'ப்', 'ம்', 'ய்', 'ர்', 'ல்', 'வ்', 'ழ்', 'ள்', 'ற்', 'ன்']
   
   In [4]: print(GRANTHA_CONSONANTS)
   Out[4]: ['ஜ்', 'ஶ்', 'ஷ்', 'ஸ்', 'ஹ்', 'க்ஷ்']



Corpora
=======

Use ``CorpusImporter()`` or browse the `CLTK GitHub organization <https://github.com/cltk>`_ (anything beginning with ``tamil_``) to discover available tamil corpora.

.. code-block:: python

   In [1]: from cltk.corpus.utils.importer import CorpusImporter

   In [2]: c = CorpusImporter('tamil')

   In [3]: c.list_corpora
   Out[3]: ['tamil_text_ptr_tipitaka']
