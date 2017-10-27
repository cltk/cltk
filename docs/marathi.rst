Marathi
********
Marathi is an Indian language spoken predominantly by the Marathi people of Maharashtra. Marathi has some of the oldest literature of all modern Indo-Aryan languages, dating from about 900 AD. Early Marathi literature written during the Yadava (850-1312 CE) was mostly religious and philosophical in nature. Dnyaneshwar (1275–1296) was the first Marathi literary figure who had wide readership and profound influence. His major works are Amrutanubhav and Bhavarth Deepika (popularly known as Dnyaneshwari), a 9000-couplet long commentary on the Bhagavad Gita. (Source: `Wikipedia <https://en.wikipedia.org/wiki/Marathi_language>`_)

Corpora
=======
Use ``CorpusImporter()`` or browse the `CLTK GitHub organization <https://github.com/cltk>`_ (anything beginning with ``marathi_``) to discover available Marathi corpora.

.. code-block:: python

   In [1]: from cltk.corpus.utils.importer import CorpusImporter

   In [2]: c = CorpusImporter('marathi')

   In [3]: c.list_corpora
   Out[3]:
   ['marathi_text_wikisource']

Tokenizer
=========
This tool can help break up a sentence into smaller constituents.

.. code-block:: python

   In [1]: from cltk.tokenize.indian_tokenizer import indian_punctuation_tokenize_regex as i_word

   In [2]: sentence = "आतां विश्वात्मके देवे, येणे वाग्यज्ञे तोषावे, तोषोनि मज द्यावे, पसायदान हे"

   In [3]: marathi_text_tokenize = i_word(sentence)

   In [4]: marathi_text_tokenize
   ['आतां', 'विश्वात्मके', 'देवे,', 'येणे', 'वाग्यज्ञे', 'तोषावे,', 'तोषोनि', 'मज', 'द्यावे,', 'पसायदान', 'हे']



